from tortoise import run_async
from aiohttp import ClientSession

from db.utils import create_database
from db.schema import User, Location
from core.logging import LOG


async def main() -> None:
    try:
        await create_database()
        users = await User.all()
        if len(users) == 100:
            return
        data_url = "https://randomuser.me/api/?results=100&seed=25cd41c01220463d"
        async with ClientSession() as session:
            async with session.get(data_url) as response:
                for obj in (await response.json())["results"]:
                    # https://api.worldbank.org/v2/country/{CODE}?format=json
                    user_data = {
                        "first_name": obj["name"]["first"],
                        "last_name": obj["name"]["last"],
                        "email": obj["email"],
                        "username": obj["login"]["username"],
                        "password": obj["login"]["password"],
                        "birthday": obj["dob"]["date"],
                        "cell": obj["cell"],
                        "gender": obj["gender"],
                        "nationality": obj["location"]["country"],
                    }
                    location_data = {
                        "street": obj["location"]["street"]["name"],
                        "street_number": obj["location"]["street"]["number"],
                        "city": obj["location"]["city"],
                        "state": obj["location"]["state"],
                        "country": obj["location"]["country"],
                        "postcode": obj["location"]["postcode"],
                    }
                    location = await Location.create(**location_data)
                    user_data["location"] = location
                    await User.create(**user_data)

    except Exception as e:
        LOG.info(f"{e}")


if __name__ == "__main__":
    run_async(main())
