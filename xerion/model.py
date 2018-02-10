from sqlalchemy.ext.declarative import declarative_base

from . import metadata, meta


class BaseModel(declarative_base(metaclass=meta.XerionMeta, metadata=metadata)):
    """Base Declarative Model"""
    __abstract__ = True
