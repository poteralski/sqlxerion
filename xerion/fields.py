from sqlalchemy import Boolean, String, Float, Integer


class Field:
    column_class = None

    def __init__(self, *args, **kwargs) -> None:
        self.args = args
        self.kwargs = kwargs


class IntField(Field):
    column_class = Integer


class FloatField(Field):
    column_class = Float


class StrField(Field):
    column_class = String


class BoolField(Field):
    column_class = Boolean
