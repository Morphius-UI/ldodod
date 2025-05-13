from peewee import *
import calendar
import time
db = SqliteDatabase('ldodod/Project/base_ldod.db')


class Person(Model): #Хранит все данные которые есть в боте
    CREATE_DATA = IntegerField()
    user_id = IntegerField()
    Points = IntegerField()
    Class = IntegerField()
    Register = CharField()
    Login = CharField()
    class Meta:
        database = db

class PROFILE(Model): #Хранит все-все данные
    CREATE_DATA = IntegerField()
    user_id = IntegerField()
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

#PROFILE.create(CREATE_DATA=None, user_id=None, Points=10000, Class=10, Register=None,Login='КозловАИ')


def pars_login_user(FIO):
    for user in USERS_BASE.select().where(USERS_BASE.USER_FIO == FIO):
        return user.USER_PASSWORD

def pars_admin_panel(Log=None, pas=None):
    if Log:
        for login in ADMIN_BASE.select().where(ADMIN_BASE.ADMIN_LOGIN == Log):
            return login.ADMIN_LOGIN
    else:
        for pas in ADMIN_BASE.select().where(ADMIN_BASE.ADMIN_PASSWORD == pas):
            return pas.ADMIN_PASSWORD

def pars_users(login=None, password=None, register=None, klass=None, points=None, _time=None, _login=None):
    if login:
        for login in USERS_BASE.select().where(USERS_BASE.USER_FIO == login):
            return login.USER_FIO
    elif password:
        for password in USERS_BASE.select().where(USERS_BASE.USER_PASSWORD == password):
            return password.USER_PASSWORD
    elif points:
        for password in Person.select().where(Person.Login == points):
            return password.Points
    elif klass:
        for klass in Person.select().where(Person.Login == klass):
            return klass.Class
    elif _time:
        for user in Person.select().where(Person.user_id == _time):
            return user.CREATE_DATA
    elif _login:
        for login in Person.select().where(Person.user_id == _login):
            return login.Login
    else:
        for register in Person.select().where(Person.Login == register):
            return register.Register

def truth(login=None, klass=None, point=None):
    if login:
        for user in PROFILE.select().where(PROFILE.Login == login):
            return user
    elif klass:
        for user in PROFILE.select().where(PROFILE.Login == klass):
            return user.Class
    elif point:
        for user in PROFILE.select().where(PROFILE.Login == point):
            return user.Points

def register(message, login, klass, password):
    point = truth(point=login)
    klass = truth(klass=login)
    Person.create(CREATE_DATA=calendar.timegm(time.gmtime()), user_id=message.chat.id, Points=point, Class=klass,
                  Register='True', Login=login)
    USERS_BASE.create(USER_FIO=login, USER_PASSWORD=password)


def admin_spisok():
    Usr = []
    Points = []
    for user in PROFILE.select():
        userId = user.user_id
        point = user.Points
        Usr.append(userId)
        Points.append(point)


    return Usr, Points
