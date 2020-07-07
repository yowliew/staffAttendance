from flask import jsonify
from flask_restful import Resource, reqparse
from models.users import UserModel
from models.employees import EmployeeModel, EClassModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument("username", type=str, required=True, help="Username Error.")
    parser.add_argument("password", type=str, required=True, help="Password Error.")

    def post(self):
        data = self.parser.parse_args()

        if UserModel.find_by_username(data["username"]):
            return jsonify({"message": "User already exist in the database."})

        user = UserModel(**data)
        user.save_to_db()

        return jsonify({"message": "User created successfully."})


class AllEmployeeList(Resource):
    def get(self):
        data = []
        for item in EmployeeModel.find_all_employee():
            data.append(item.json())
        return data


class EmployeeRegister(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument("emp_id", type=int, required=True, help="Username Error.")
    parser.add_argument("full_name", type=str, required=True, help="Name Error.")
    parser.add_argument("emp_class", type=str, required=True, help="Emp_class Error.")
    parser.add_argument("hire_date", required=True, help="hire_date Error.")
    parser.add_argument("emp_salary", required=True, help="Salary Error.")
    parser.add_argument("active_flag", type=str, required=True, help="Active_flag Error.")

    def post(self):
        data = self.parser.parse_args()

        employee = EmployeeModel.find_by_id(data["emp_id"])
        if employee:
            employee.full_name = data["full_name"]
            employee.emp_class = data["emp_class"]
            employee.hire_date = data["hire_date"]
            employee.emp_salary = float(data["emp_salary"])

            employee.active_flag = "Y" if data["active_flag"] == "Yes" else "N"

            employee.save_to_db()

            return jsonify({"message": "Employee updated."})

        employee = EmployeeModel(emp_id=data["emp_id"], full_name=data["full_name"], hire_date=data["hire_date"],
                                 emp_salary=float(data["emp_salary"]), emp_class=data["emp_class"], active_flag='Y',
                                 first_name="",
                                 last_name="", hash_val=None, thumb_id=None)
        employee.save_to_db()
        return jsonify({"message": "Employee created successfully."})


class AllEmpClassList(Resource):
    def get(self):
        data = []
        for item in EClassModel.find_all_class():
            data.append(item.json())
        return data


class EmpClassRegister(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument("emp_class", type=str, required=True, help="Username Error.")
    parser.add_argument("emp_desc", type=str, required=True, help="Class Name Error.")
    parser.add_argument("max_working", required=True, help="Max working hour Error.")
    parser.add_argument("ot_after", required=True, help="OT working hour Error.")
    parser.add_argument("ot_rate", required=True, help="OT rate Error.")
    parser.add_argument("active_flag", type=str, required=True, help="Active_flag Error.")

    def post(self):
        data = self.parser.parse_args()

        empClass = EClassModel.find_by_class(data["emp_class"])
        if empClass:
            empClass.emp_desc = data["emp_desc"]
            empClass.max_working = float(data["max_working"])
            empClass.ot_after = float(data["ot_after"])
            empClass.ot_rate = float(data["ot_rate"])

            empClass.active_flag = "Y" if data["active_flag"] == "Yes" else "N"

            empClass.save_to_db()

            return jsonify({"message": "Employee updated."})

        empclass = EClassModel(emp_class=data["emp_class"], emp_desc=data["emp_desc"],
                               max_working=float(data["max_working"]),
                               ot_after=float(data["ot_after"]), ot_rate=float(data["ot_rate"]), active_flag='Y')
        empclass.save_to_db()

        return jsonify({"message": "Employee created successfully."})
