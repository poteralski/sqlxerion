from xerion.extensions import DataBase
from pytest import fixture


@fixture
def db() -> DataBase:
    return DataBase()
