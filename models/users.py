from typing import Dict
from flask import session
from common.db import db1
from models.ancestor import Ancestor
import common.errors as UserErrors


class UserModel(Ancestor, db1.Model):
    __tablename__ = "users"

    id = db1.Column(db1.Integer, primary_key=True)
    username = db1.Column(db1.String(80), index=True, nullable=False)
    password = db1.Column(db1.String(80), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.add_user = ""
        self.upd_user = ""  # TODO to be implemented

    def json(self) -> Dict:
        return {
            "username": self.username,
            "password": self.password
        }

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all_user(cls):
        return cls.query.all()

    @staticmethod
    def is_user_valid(username, password):
        data = UserModel.find_by_username(username)
        if data is not None:
            if data.password != password:
                raise UserErrors.IncorrectPasswordError("Password not correct")
        else:
            raise UserErrors.UserNotFoundError('User not Found in Database')
