from peewee import *
import bcrypt
from datetime import datetime

db = SqliteDatabase('D:/pc.db')


class User(Model):
    username = CharField(100)
    password_hash = TextField()
    password_salt = TextField()
    last_login = DateTimeField()
    profile_picture = BlobField()

    class Meta:
        database = db


class Messages(Model):
    sender = CharField(100)
    destination = CharField(100)
    message_text = TextField(100)
    attachments = BlobField(null=True)
    timestamp = DateTimeField()


def add_user(username, password, pfp_byte_arr):
    try:
        query = User.get(User.username == username)
    except User.DoesNotExist:
        salt = bcrypt.gensalt()
        pwd = bcrypt.hashpw(password.encode(), salt)
        new_user = User(username=username, password_hash=pwd, password_salt=salt, last_login=datetime.now(),
                        profile_picture=pfp_byte_arr)
        new_user.save()
    else:
        return False


def login(username, password):
    try:
        query = User.get(User.username == username)
    except User.DoesNotExist:
        return False
    else:
        encrypted = query.password_hash.encode()
        salt = query.password_salt.encode()
        if bcrypt.hashpw(password.encode(), salt) == encrypted:
            query.last_login = datetime.now()
            query.save()
            return True
        else:
            return False


def delete_user(username, password):
    if login(username, password):
        User.delete().where(User.username == username).execute()
        return True
    return False


if __name__ == '__main__':
    pass
