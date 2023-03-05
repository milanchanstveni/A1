from tortoise.contrib.pydantic import (
    pydantic_model_creator,
    pydantic_queryset_creator
)

from db.schema import (
    User,
    Location
)

UserModel = pydantic_model_creator(User, name="User")
LocationModel = pydantic_model_creator(Location, name="Location")

UserQuerySet = pydantic_queryset_creator(User, name="UserQuerySet")
LocationQuerySet = pydantic_queryset_creator(Location, name="LocationQuerySet")
