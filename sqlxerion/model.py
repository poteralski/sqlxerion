from sqlalchemy.ext.declarative import declarative_base

from sqlxerion.meta import PrimaMateria


def xerion_base(metadata):
    class BaseModel(declarative_base(metaclass=PrimaMateria, metadata=metadata)):
        __abstract__ = True

    return BaseModel
