from tortoise.models import Model
from tortoise import fields


class Location(Model):
    street = fields.TextField()
    street_number = fields.IntField()
    city = fields.TextField()
    state = fields.TextField()
    country = fields.TextField()
    postcode = fields.TextField()

    def __str__(self):
        return f"Location: {self.street} {self.street_number}({self.city})"


class User(Model):
    id = fields.IntField(pk=True)
    first_name = fields.TextField()
    last_name = fields.TextField()
    email = fields.TextField()
    username = fields.TextField()
    password = fields.TextField()
    birthday = fields.DateField()
    nationality = fields.TextField()
    cell = fields.TextField()
    gender = fields.TextField()
    location = fields.ForeignKeyField("models.Location", related_name="users")

    def __str__(self):
        return f"User {self.first_name} {self.last_name}"
