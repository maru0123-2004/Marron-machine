from tortoise.models import Model
from tortoise.fields import CharField

class Token(Model):
    token = CharField(pk=True, max_length=200, description="Token")
    user_id = CharField(null=False, max_length=200)