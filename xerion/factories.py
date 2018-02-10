from sqlalchemy import orm as sqla_orm
from sqlalchemy.ext import declarative
import sqlalchemy as sqla
from .utils import get_model


def fields_factory(column_class, args, kwargs):
    """
    This method is responsible for creating columns.
    """
    return sqla.Column(column_class(*args), **kwargs)


def assoc_table_factory(self, instance_table_name, tablename, attr_name):
    """
    This method is responsible for creating association tables.
    """
    return sqla.Table(
        tablename,
        self.metadata,
        sqla.Column(
            'left_id', sqla.Integer,
            sqla.ForeignKey(f'{self.__tablename__}.id')),
        sqla.Column(
            'right_id',
            sqla.Integer,
            sqla.ForeignKey(f'{instance_table_name}.id')
        ),
        sqla.PrimaryKeyConstraint(
            'left_id',
            'right_id',
            name=f'{self.__tablename__}_{attr_name}_assoc_pk'
        )
    )


def many_to_many_factory(cls, instance, secondary, secondary_tablename, is_abstract, attr_name):
    """
    This method is responsible for creating required M2M objects.
    """
    secondary = instance.extra.pop('secondary', None)
    secondary_tablename = f'{cls.__tablename__}_{attr_name}'

    if not is_abstract:
        # create backref if is not abstract
        setattr(
            get_model(cls, instance.model),
            instance.extra.pop('backref', cls.__tablename__),
            sqla_orm.relationship(cls, secondary=secondary_tablename)
        )

    return declarative.declared_attr(
        lambda self, instance=instance, secondary=secondary:
        sqla_orm.relationship(
            instance.model,
            secondary=secondary or assoc_table_factory(
                self,
                get_model(self, instance.model).__tablename__,
                secondary_tablename,
                attr_name
            ),
            **instance.extra
        )
    )


def foreign_key_column_factory(model, nullable, primary_key, extra):
    return declarative.declared_attr(
        lambda self, model=model, nullable=nullable, primary_key=primary_key:
        sqla.Column(
            sqla.Integer,
            sqla.ForeignKey(f'{get_model(self, model).__tablename__}.id'),
            nullable=nullable,
            primary_key=primary_key
        )
    )


def foreign_key_rel_factory(model,  nullable, primary_key, extra):
    return declarative.declared_attr(
        lambda self, model=model, extra=extra:
        sqla_orm.relationship(
            model,
            **extra
        )
    )
