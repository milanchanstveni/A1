"""Extract data from external sources."""

from typing import Any, Dict, List
from aiohttp import ClientSession

from db.schema import User
from core.logging import LOG


async def get_external_users() -> List[Dict[str, Any]]:
    """Get users from external API."""
    try:
        data_url = "https://randomuser.me/api/?results=100&seed=25cd41c01220463d"
        async with ClientSession() as session:
            async with session.get(data_url) as response:
                return (await response.json())["results"]

    except Exception as e:
        LOG.info(f"{e}")
        return []


async def get_nationality(coutry_code: str) -> str:
    """Get full name of the country from country code."""
    try:
        data_url = f"https://api.worldbank.org/v2/country/{coutry_code}?format=json"
        async with ClientSession() as session:
            async with session.get(data_url) as response:
                return (await response.json())[1][0]["name"]

    except Exception as e:
        LOG.info(f"{e}")
        return ""


async def db_user_count() -> int:
    """Get the number of users in the database."""
    try:
        users = await User.all()
        return len(users)

    except Exception as e:
        LOG.info(f"{e}")
        return -1
