from typing import Dict
from flask import session
from common.db import db1
from models.ancestor import Ancestor


class EmployeeModel(Ancestor, db1.Model):
    __tablename__ = "employee"

    id = db1.Column(db1.Integer, primary_key=True)
    emp_id = db1.Column(db1.Integer, index=True, nullable=False)
    first_name = db1.Column(db1.String(100), index=True)
    last_name = db1.Column(db1.String(100), index=True)
    full_name = db1.Column(db1.String(200), index=True, nullable=False)
    hire_date = db1.Column(db1.String(50))
    emp_salary = db1.Column(db1.DECIMAL(4, 2))
    hash_val = db1.Column(db1.String(100), nullable=True)
    thumb_id = db1.Column(db1.Integer, index=True)
    active_flag = db1.Column(db1.String(1))
    emp_class = db1.Column(db1.String(50), db1.ForeignKey("emp_class.emp_class"), nullable=False)
    empclass = db1.relationship("EClassModel")

    def __init__(self, emp_id, first_name, last_name, full_name, hire_date, emp_salary, emp_class, active_flag,
                 hash_val=None, thumb_id=None):
        self.emp_id = emp_id
        self.first_name = first_name
        self.last_name = last_name
        self.full_name = full_name
        self.hire_date = hire_date
        self.emp_salary = emp_salary
        self.emp_class = emp_class
        self.hash_val = hash_val
        self.thumb_id = thumb_id
        self.active_flag = active_flag
        self.add_user = session["username"] if "username" in session else ""

    def json(self) -> Dict:
        return {
            "emp_id": self.emp_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.full_name,
            "hire_date": self.hire_date,
            "emp_salary": str(self.emp_salary),
            "emp_class": self.emp_class,
            "hash_val": self.hash_val,
            "thumb_id": self.thumb_id,
            "active_flag": self.active_flag
        }

    @classmethod
    def find_by_id(cls, emp_id):
        return cls.query.filter_by(emp_id=emp_id).first()

    @classmethod
    def find_all_employee(cls):
        return cls.query.all()


class EClassModel(Ancestor, db1.Model):
    __tablename__ = "emp_class"

    id = db1.Column(db1.Integer, primary_key=True)
    emp_class = db1.Column(db1.String(50), index=True, nullable=False)
    emp_desc = db1.Column(db1.String(100), nullable=False)
    max_working = db1.Column(db1.DECIMAL(4, 2), nullable=False)
    ot_after = db1.Column(db1.DECIMAL(4, 2), nullable=False)
    ot_rate = db1.Column(db1.DECIMAL(4, 2), nullable=False)
    active_flag = db1.Column(db1.String(1), nullable=False)

    def __init__(self, emp_class, emp_desc, max_working, ot_after, ot_rate, active_flag):
        self.emp_class = emp_class
        self.emp_desc = emp_desc
        self.max_working = max_working
        self.ot_after = ot_after
        self.ot_rate = ot_rate
        self.active_flag = active_flag
        self.add_user = session["username"] if "username" in session else ""

    def json(self) -> Dict:
        return {
            "id": self.id,
            "emp_class": self.emp_class,
            "emp_desc": self.emp_desc,
            "max_working": str(self.max_working),
            "ot_after": str(self.ot_after),
            "ot_rate": str(self.ot_rate),
            "active_flag": self.active_flag
        }

    @classmethod
    def find_by_class(cls, emp_class):
        return cls.query.filter_by(emp_class=emp_class).first()

    @classmethod
    def find_all_class(cls):
        return cls.query.all()
