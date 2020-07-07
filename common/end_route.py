# import for api
from resources.validate import Validate
from resources.misc import Logout, AutoComplete, PopulateDropdown
from resources.register import UserRegister, AllEmployeeList, EmployeeRegister, EmpClassRegister, AllEmpClassList

# import for blueprint
from views.users import user_blueprint
from views.employees import employees_blueprint
from views.fingerscan import fingerscan_blueprint


def api_end_route(api):
    api.add_resource(Validate, "/validate_field")
    api.add_resource(Logout, "/logout")
    api.add_resource(AutoComplete, "/autocomplete")
    api.add_resource(UserRegister, "/user_register")
    api.add_resource(AllEmployeeList, "/employee_list")
    api.add_resource(EmployeeRegister, "/employee_register")
    api.add_resource(PopulateDropdown, "/populate_dropdown")
    api.add_resource(EmpClassRegister, "/empClass_register")
    api.add_resource(AllEmpClassList, "/empClass_list")


def blueprint_end_route(app):
    app.register_blueprint(user_blueprint, url_prefix="/")
    app.register_blueprint(user_blueprint, url_prefix="/users")
    app.register_blueprint(employees_blueprint, url_prefix="/employees")
    app.register_blueprint(employees_blueprint, url_prefix="/employees/class")
    app.register_blueprint(fingerscan_blueprint, url_prefix="/fingerscan")
    # app.register_blueprint(fingerscan_blueprint, url_prefix="/fingerscan/scan")