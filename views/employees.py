from flask import Blueprint, request, session, url_for, render_template, redirect, flash, current_app
from models.employees import EmployeeModel

employees_blueprint = Blueprint('employees', __name__)


@employees_blueprint.route('/maint', methods=['GET', 'POST'])
def maint_employees():
    if request.method == 'GET':
        return render_template("employees/register.html")


@employees_blueprint.route('/class_maint', methods=['GET'])
def maint_emp_class():
    if request.method == 'GET':
        return render_template("employees/emp_class.html")
