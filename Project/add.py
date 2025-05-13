from peewee import *
import calendar
import time
db = SqliteDatabase('ldodod/Project/base_ldod.db')


class Person(Model): #Хранит все данные которые есть в боте, кто зарегистрирован
    CREATE_DATA = IntegerField()
    user_id = IntegerField()
    Points = IntegerField()
    Class = IntegerField()
    Register = CharField()
    Login = CharField()
    class Meta:
        database = db

class PROFILE(Model): #Хранит все-все данные о учениках в заведении
    Points = IntegerField()
    Class = IntegerField()
    Register = CharField()
    Login = CharField()
    class Meta:
        database = db

class ADMIN_BASE(Model): #админ панель
    ADMIN_LOGIN = CharField()
    ADMIN_PASSWORD = CharField()
    class Meta:
        database = db

class USERS_BASE(Model):
    USER_FIO = CharField()
    USER_PASSWORD = CharField()
    class Meta:
        database = db


db.create_tables([Person, ADMIN_BASE, USERS_BASE, PROFILE])

PROFILE.create(Points=12312, Class=11, Login='ЗвонаревА', Register=False)