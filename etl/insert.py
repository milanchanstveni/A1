"""Load data into the database."""

from typing import Any, Dict

from db.schema import User, Location
from core.logging import LOG


async def load_location(data: Dict[str, Any]) -> Location | None:
    """Load locations into the database."""
    try:
        return await Location.create(**data)
    except Exception as e:
        LOG.info(f"{e}")
        return None


async def load_user(data: Dict[str, Any]) -> User | None:
    """Load users into the database."""
    try:
        return await User.create(**data)
    except Exception as e:
        LOG.info(f"{e}")
        return None
