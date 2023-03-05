from tortoise import Tortoise
from typing import Dict, Any
import asyncio

from core.env import env
from db.exceptions import (
    InitError,
    CloseError,
    DatabaseError
)
from core.logging import LOG
from db.schema import (
    User,
    Location
)


db_url = "{}://{}:{}@{}:{}/{}".format(
        env("DB_SCHEME"),
        env("DB_USER"),
        env("DB_PASSWORD"),
        env("DB_HOST"),
        env("DB_PORT"),
        env("DB_NAME"),
)

if env("DEBUG") in ["1", 1, True, "true", "on", "yes"]:
    # db_url = "sqlite:///db.sqlite3"
    db_url = "sqlite://:memory:"


async def create_database() -> None:
    """Connect to the database and create the tables if they don't exist."""
    try:
        await asyncio.sleep(10)
        await Tortoise.init(
            db_url=db_url,
            modules={'models': ['db.schema']}
        )
        await Tortoise.generate_schemas()
    except Exception as e:
        LOG.info(f"{e}")
        raise InitError(str(e))


def get_db_config() -> Dict[str, Any]:
    """Get the database configuration."""
    return {
        "connections": {
            "default": db_url
        },
        "apps": {
            "models": {
                "models": ["db.schema", "aerich.models"],
                "default_connection": "default"
            }
        }
    }


CONFIG = get_db_config()


async def close() -> None:
    """Close all database connections."""
    try:
        await Tortoise.close_connections()
    except Exception as e:
        LOG.info(f"{e}")
        raise CloseError(str(e))


async def delete_all_records() -> None:
    """Delete all records."""
    try:
        await User.all().delete()
        await Location.all().delete()
    except Exception as e:
        LOG.info(f"{e}")
        raise DatabaseError(str(e))
