from peewee import *
from playhouse.db_url import connect
from config import DATABASE

database = connect(DATABASE)

class BaseModel(Model):
    class Meta:
        database = database


class TapTapApp(BaseModel):
    name = CharField(max_length=255, )
    appId = IntegerField(unique=True)
    score = DecimalField()

class Review(BaseModel):
    app = ForeignKeyField(TapTapApp)
    reviewId = CharField(unique=True)
    text = TextField()
    star = IntegerField()

class RunLog(BaseModel):
    app = ForeignKeyField(TapTapApp, unique=True)
    page = IntegerField()


if __name__ == "__main__":
    with database:
        database.create_tables([TapTapApp, Review, RunLog])
