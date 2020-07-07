from flask import Blueprint, request, render_template
import common.socketio_route as socketio

fingerscan_blueprint = Blueprint('fingerscan', __name__)


@fingerscan_blueprint.route('/maint', methods=['GET'])
def maint_employees():
    if request.method == 'GET':
        return render_template("employees/fingerscan.html")
