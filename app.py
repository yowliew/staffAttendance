import os
from flask_restful import Api

from common.end_route import api_end_route, blueprint_end_route
from pre_app import app, socketio
import common.socketio_route  # do not delete

application = app

if os.environ["ENV"] == "development":
    app.config.from_object("config.DevelopmentConfig")
elif os.environ["ENV"] == "testing":
    app.config.from_object("config.TestingConfig")
else:
    app.config.from_object("config.ProductionConfig")

print(f'This is from app.config: {app.config["ENV"]}')
print(app.config["DB_NAME"])
print(app.config["DB_CONNECTION_STRING"])

app.config["SQLALCHEMY_DATABASE_URI"] = app.config["DB_CONNECTION_STRING"]
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = app.config["SECRET_KEY"]

api = Api(app)
api_end_route(api)
blueprint_end_route(app)

if __name__ == "__main__":
    from common.db import db1

    db1.init_app(app)


    @app.before_first_request
    def create_dbstruc():
        db1.create_all()


    # app.run()
    socketio.run(app, debug=True)
