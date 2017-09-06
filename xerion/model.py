from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapper

from xerion import metadata
from xerion.meta import PrimaMateria


class BaseModel(declarative_base(metaclass=PrimaMateria, metadata=metadata, mapper=mapper)):
    """Base Declarative Model"""
    __abstract__ = True
