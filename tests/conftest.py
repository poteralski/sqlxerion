from typing import NamedTuple

from xerion.extensions import DataBase
from pytest import fixture


@fixture
def app():
    class App(NamedTuple):
        config: dict

    return App(config={'SQLALCHEMY_DATABASE_URI': 'sqlite://'})


@fixture
def db(app) -> DataBase:
    db = DataBase()
    db.init_app(app)
    yield db
    db.session.close_all()
    db.metadata.drop_all()
