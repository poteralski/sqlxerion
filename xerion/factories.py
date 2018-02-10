from sqlalchemy import orm as sqla_orm
from sqlalchemy.ext import declarative
import sqlalchemy as sqla

from .utils import get_model


def fields_factory(instance):
    return sqla.Column(
        instance.column_class(*instance.args),
        **instance.kwargs
    )


def many_to_many_factory(cls, instance, is_abstract, attr_name):
    assoc_table = instance.extra.pop('secondary', None)

    def get_relationship(self, instance=instance, assoc_table=assoc_table):
        instance_model = get_model(self, instance.model)
        instance_table_name = instance_model.__tablename__
        return sqla_orm.relationship(
            instance.model,
            secondary=assoc_table or sqla.Table(
                f'{self.__tablename__}_{attr_name}',
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
            ),
            **instance.extra
        )

    if not is_abstract:
        setattr(
            get_model(cls, instance.model),
            instance.extra.pop('backref', cls.__tablename__),
            sqla_orm.relationship(cls, secondary=f'{cls.__tablename__}_{attr_name}')
        )
    return declarative.declared_attr(get_relationship)


def foreign_key_factory(instance, key, new_attrs):
    def get_column(self, instance=instance):
        instance_model = get_model(self, instance.model)
        instance_table_name = instance_model.__tablename__
        return sqla.Column(
            sqla.Integer,
            sqla.ForeignKey(f'{instance_table_name}.id'),
            nullable=instance.nullable,
            primary_key=instance.primary_key
        )

    new_attrs[f'{key}_id'] = declarative.declared_attr(get_column)
    new_attrs[key] = declarative.declared_attr(
        lambda self, instance=instance: sqla_orm.relationship(
            instance.model,
            **instance.extra
        )
    )
