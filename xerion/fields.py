import sqlalchemy


class Field:
    column_class = None

    def __init__(self, *args, **kwargs) -> None:
        self.args = args
        self.kwargs = kwargs


class IntField(Field):
    column_class = sqlalchemy.Integer


class FloatField(Field):
    column_class = sqlalchemy.Float


class StrField(Field):
    column_class = sqlalchemy.String


class BoolField(Field):
    column_class = sqlalchemy.Boolean
