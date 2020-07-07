from typing import Dict
from flask import session
from common.db import db1
from models.ancestor import Ancestor


class TimeTrackModel(Ancestor, db1.Model):
    __tablename__ = "time_tracker"

    id = db1.Column(db1.Integer, primary_key=True)
    emp_id = db1.Column(db1.Integer, db1.ForeignKey("employee.emp_id"), index=True, nullable=False)
    start_time = db1.Column(db1.DateTime(timezone=True), index=True, nullable=False)
    end_time = db1.Column(db1.DateTime(timezone=True), index=True, nullable=False)
    duration = db1.Column(db1.DECIMAL(4, 2), nullable=False)
    employee = db1.relationship("EmployeeModel")

    def __init__(self, emp_id, start_time, end_time, duration):
        self.emp_id = emp_id
        self.start_time = start_time
        self.end_time = end_time
        self.duration = duration
        self.add_user = ""
        self.upd_user = ""  # TODO to be implemented

    def json(self) -> Dict:
        return {
            "emp_id": self.emp_id,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "duration": self.duration,
        }

    @classmethod
    def find_by_id(cls, emp_id):
        return cls.query.filter_by(emp_id=emp_id).first()

    @classmethod
    def find_all_by_date(cls, find_date):
        ## TODO need to recheck this
        return cls.query.filter(cls.start_time >= find_date, cls.end_time <= find_date + 12).all()
