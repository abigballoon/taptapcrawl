from peewee import *
from playhouse.db_url import connect
from config import NIGHT_DATABASE

database = Proxy()

class BaseMeta(Model):
    database = database

class Post(Model):
    content = TextField(null=True, column_name="post_content")
    post_date = DateTimeField(null=True)

    class Meta(BaseMeta):
        table_name = "post"

class Weibo(Model):
    content = TextField(null=True, column_name="subject")
    post_date = DateTimeField(null=True)

    class Meta(BaseMeta):
        table_name = "weibo"

class Thread(Model):
    content = TextField(null=True, column_name="subject")
    post_date = DateTimeField(null=True, column_name="postDate")

    class Meta(BaseMeta):
        table_name = "thread"

def use(project):
    return connect(NIGHT_DATABASE%project)
