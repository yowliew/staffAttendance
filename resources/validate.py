from flask_restful import Resource, reqparse
from flask import jsonify
import re
from models.users import UserModel
from models.employees import EmployeeModel, EClassModel


class Validate(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument("method", type=str, required=True, help="Method Error")
    parser.add_argument("value", type=str, required=True, help="Value Error.")

    method = None
    value = None

    def post(self):
        data = self.parser.parse_args()
        self.method = data["method"]
        self.value = data["value"]
        return self.redirect(self.method)

    def redirect(self, method):
        switcher = {
            "username": self.username,
            "password": self.password,
            "emp_id": self.emp_id,
            "emp_class":self.emp_class,
            "nothing": lambda: 'XXX'
        }
        func = switcher.get(method, lambda: 'Invalid')
        return func()

    def emp_class(self):
        if EClassModel.find_by_class(self.value):
            return jsonify({"message": False, "error": "Employee Class already exist in the database."})
        else:
            return jsonify({"message": True})

    def username(self):  # Return True only when passed field validate

        if UserModel.find_by_username(self.value):
            return jsonify({"message": False, "error": "User already exist in the database."})
        else:
            return jsonify({"message": True})

    def password(self):
        string_check = re.compile("[@_!#$%^&*()<>?/\|}{~:]")
        if string_check.search(self.value) is None:
            return jsonify({"message": False, "error": "Password must contains special character."})
        else:
            return jsonify({"message": True})

    def emp_id(self):
        if EmployeeModel.find_by_id(self.value):
            return jsonify({"message": False, "error": "Employee Number already exist in the database."})
        else:
            return jsonify({"message": True})

