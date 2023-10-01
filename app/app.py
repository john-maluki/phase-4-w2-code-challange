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

power_input_model = api.model("Power", {"description": fields.String})

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

hero_power_model = api.model(
    "HeroPower",
    {
        "id": fields.Integer,
        "strength": fields.String,
        "power_id": fields.Integer,
        "hero_id": fields.Integer,
    },
)

hero_power_input_model = api.model(
    "HeroPower",
    {
        "strength": fields.String,
        "power_id": fields.Integer,
        "hero_id": fields.Integer,
    },
)


@api.errorhandler(ObjectNotFoundException)
def handle_no_result_exception(error):
    """Return a custom not found error message and 404 status code"""
    return {"error": error.message}, 404


@api.errorhandler(ValueError)
def handle_no_result_exception(error):
    """Return a custom not found error message and 404 status code"""
    return {"errors": error.args}, 400


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


@ns.route("/powers")
class PowerResource(Resource):
    @ns.marshal_list_with(power_model)
    def get(self):
        return Power.query.all()


@ns.route("/powers/<int:id>")
class PowerByIdResource(Resource):
    @ns.marshal_with(power_model)
    def get(self, id):
        power = Power.query.filter_by(id=id).first()
        if not power:
            raise ObjectNotFoundException("Power not found")
        else:
            return power

    @ns.expect(power_input_model)
    @ns.marshal_with(power_model)
    def patch(self, id):
        power = Power.query.filter_by(id=id).first()
        if not power:
            raise ObjectNotFoundException("Power not found")
        else:
            try:
                for attr in ns.payload:
                    setattr(power, attr, ns.payload[attr])
                db.session.add(power)
                db.session.commit()
                return power
            except ValueError as e:
                raise e


@ns.route("/hero_powers")
class HeroPowerResource(Resource):
    @ns.marshal_list_with(hero_power_model)
    def get(self):
        return HeroPower.query.all()

    @ns.expect(hero_power_input_model)
    @ns.marshal_with(single_hero_model)
    def post(self):
        try:
            hero_power = HeroPower(
                strength=ns.payload["strength"],
                power_id=ns.payload["power_id"],
                hero_id=ns.payload["hero_id"],
            )
            db.session.add(hero_power)
            db.session.commit()
            hero = Hero.query.filter_by(id=ns.payload["hero_id"]).first()
            return hero, 201
        except ValueError as e:
            raise e


if __name__ == "__main__":
    app.run(port=5555)
