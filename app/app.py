#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate
from flask_restx import Api, Resource, Namespace, fields

from models import db, Hero, Power, HeroPower
from exceptions import ObjectNotFoundException

ns = Namespace("/")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

migrate = Migrate(app, db)

db.init_app(app)
api = Api(app)
api.add_namespace(ns)

power_model = api.model(
    "Power", {"id": fields.Integer, "name": fields.String, "description": fields.String}
)

hero_model = api.model(
    "Hero",
    {"id": fields.Integer, "name": fields.String, "super_name": fields.String},
)

single_hero_model = api.model(
    "Hero",
    {
        "id": fields.Integer,
        "name": fields.String,
        "super_name": fields.String,
        "powers": fields.Nested(power_model),
    },
)


@api.errorhandler(ObjectNotFoundException)
def handle_no_result_exception(error):
    """Return a custom not found error message and 404 status code"""
    return {"error": error.message}, 404


@ns.route("/heroes")
class HeroResource(Resource):
    @ns.marshal_list_with(hero_model)
    def get(self):
        return Hero.query.all()


@ns.route("/heroes/<int:id>")
class HeroByIdResource(Resource):
    @ns.marshal_with(single_hero_model)
    def get(self, id):
        hero = Hero.query.filter_by(id=id).first()
        if not hero:
            raise ObjectNotFoundException("Hero not found")
        else:
            return hero


if __name__ == "__main__":
    app.run(port=5555)
