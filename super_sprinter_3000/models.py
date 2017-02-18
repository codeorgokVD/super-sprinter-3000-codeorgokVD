from super_sprinter_3000.connectdatabase import ConnectDatabase
from peewee import *


class BaseModel(Model):
    """This class will use our postgresql database"""
    class Meta:
        db = ConnectDatabase.db


class Stories(BaseModel):
    title = CharField()
    user_story = CharField()
    acceptance_criteria = CharField()
    business_value = IntegerField()
    estimated_time = FloatField()
    status = CharField()

class Options(BaseModel):
    status = CharField()