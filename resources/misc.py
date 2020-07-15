from flask_restful import Resource, reqparse
from flask import session, jsonify
from models.employees import EClassModel, EmployeeModel


# from models.master import StateModel, ZipModel


class Logout(Resource):
    def get(self):
        session["username"] = None
        return jsonify({"message": True})


class PopulateDropdown(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("field", type=str, required=True, help="Field Error.")

    field = None

    def post(self):
        data = self.parser.parse_args()
        self.field = data["field"]
        return self.redirect(self.field)

    def redirect(self, field):
        switcher = {
            "emp_class": self.emp_class,
            "theEmployee": self.theEmployee
        }
        func = switcher.get(field, lambda: 'Invalid')
        return func()

    def emp_class(self):
        data = []
        for item in EClassModel.find_all_class():
            # print(item.emp_class)
            # json_string = "{" + "id:" + str(item.id) + "," + "emp_class:" + item.emp_class + "}"
            json_string = {"id": str(item.id), "name": item.emp_class}
            data.append(json_string)
        return data

    def theEmployee(self):
        data = []
        for item in EmployeeModel.find_all_active_employee():
            # print(item.emp_class)
            # json_string = "{" + "id:" + str(item.id) + "," + "emp_class:" + item.emp_class + "}"
            json_string = {"id": str(item.emp_id), "name": item.full_name}
            data.append(json_string)
        return data


class AutoComplete(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("field", type=str, required=True, help="Field Error.")

    field = None

    def post(self):
        data = self.parser.parse_args()
        self.field = data["field"]
        return self.redirect(self.field)

    def redirect(self, field):
        switcher = {
            "state": self.state,
            "postcode": self.postcode,
            "nothing": lambda: 'XXX'
        }
        func = switcher.get(field, lambda: 'Invalid')
        return func()

    # def state(self):
    #     states = StateModel.find_all_state()
    #     return jsonify({"state": [state.json() for state in states]})
    #
    # def postcode(self):
    #     postcodes = ZipModel.find_all_postcode()
    #     return jsonify({"postcode": [postcode.json() for postcode in postcodes]})
