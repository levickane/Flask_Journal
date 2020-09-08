from peewee import *

import datetime

DATABASE = SqliteDatabase('my_journal.db')

class Entry(Model):
    entry_id = IntegerField(primary_key=True, unique=True)
    title = CharField(max_length=200, default = "Journal Entry")
    timestamp = DateTimeField(default=datetime.datetime.now)
    timespent = IntegerField()
    stuff_learned = TextField()
    resources_to_remember = TextField()

    class Meta:
        database = DATABASE
        order_by = ('-timestamp')

    @classmethod
    def create_entry(cls, title, stuff_learned):
        cls.create(title=title, stuff_learned=stuff_learned)


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Entry], safe=True)
    DATABASE.close()
    