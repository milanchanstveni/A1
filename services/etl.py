from tortoise import run_async

from db.utils import (
    create_database,
    delete_all_records
)
from etl.gather import (
    db_user_count,
    get_external_users,
    get_nationality
)
from etl.insert import (
    load_location,
    load_user
)
from etl.exeptions import (
    GatherError,
    LoadError
)
from db.exceptions import DatabaseError
from core.logging import LOG


async def main() -> None:
    try:
        LOG.info("Starting ETL process.")
        await create_database()

        count = await db_user_count()

        if count in [100, -1]:
            if count == -1:
                raise DatabaseError("Failed to get user count.")

            return

        await delete_all_records()
        data = await get_external_users()

        if len(data) == 0:
            raise GatherError(
                message="No data received from external source.",
                source="https://randomuser.me"
            )

        for obj in data:
            nationality = obj["location"]["country"]
            # nationality = await get_nationality(obj["nat"])
            if len(nationality) == 0:
                raise GatherError(
                    message="No data received from external source.",
                    source="https://api.worldbank.org"
                )

            user_data = {
                "first_name": obj["name"]["first"],
                "last_name": obj["name"]["last"],
                "email": obj["email"],
                "username": obj["login"]["username"],
                "password": obj["login"]["password"],
                "birthday": obj["dob"]["date"],
                "cell": obj["cell"],
                "gender": obj["gender"],
                "nationality": nationality,
            }
            location_data = {
                "street": obj["location"]["street"]["name"],
                "street_number": obj["location"]["street"]["number"],
                "city": obj["location"]["city"],
                "state": obj["location"]["state"],
                "country": obj["location"]["country"],
                "postcode": obj["location"]["postcode"],
            }
            location = await load_location(location_data)
            if location is None:
                raise LoadError("Failed to load location data.")

            user_data["location"] = location
            user = await load_user(user_data)

            if user is None:
                raise LoadError("Failed to load user data.")

        LOG.info("ETL process completed.")

    except Exception as e:
        LOG.info(f"{e}")


if __name__ == "__main__":
    run_async(main())
