from db.schema import (
    User
)
from api.utils.crud import CRUD


class UserRouter(CRUD):
    class Meta:
        model = User
        path = "/users"


API = UserRouter()
