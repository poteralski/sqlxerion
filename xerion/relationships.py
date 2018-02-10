from .base import BaseXerion


class Relationship(BaseXerion):
    def __init__(self, model, *args, nullable=True, primary_key=False,
                 **kwargs) -> None:
        self.model = model
        self.extra = kwargs or {}
        self.nullable = nullable
        self.primary_key = primary_key


class ManyToMany(Relationship):
    """Helper class for ManyToMany relations"""


class ForeignKey(Relationship):
    """Helper class for ForeignKey relations"""


class OneToMany(Relationship):
    """Helper class for OneToMany relations"""
    # TODO: create required relationships


class ManyToOne(Relationship):
    """Helper class for ManyToOne relations"""
    # TODO: create required relationships


class OneToOne(Relationship):
    """Helper class for OneToOne relations"""
    # TODO: create required relationships
