from flask import Blueprint, request, render_template
from models.decorators import requires_login

employees_blueprint = Blueprint('employees', __name__)


@employees_blueprint.route('/maint', methods=['GET', 'POST'])
@requires_login
def maint_employees():
    if request.method=='GET':
        return render_template("employees/register.html")


@employees_blueprint.route('/class_maint', methods=['GET'])
@requires_login
def maint_emp_class():
    if request.method=='GET':
        return render_template("employees/emp_class.html")
