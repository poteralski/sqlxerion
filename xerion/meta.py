from sqlalchemy.ext import declarative
from sqlalchemy import orm as sqla_orm
import sqlalchemy as sqla

from .utils import get_model
from . import fields, relationships


class XerionMeta(declarative.DeclarativeMeta):
    def __init__(cls, classname, bases, dict_):
        new_attrs = dict()

        for key, instance in dict_.items():

            is_abstract = dict_.get('__abstract__', False)

            if isinstance(instance, relationships.ManyToMany):
                association_table = instance.extra.pop('secondary', None)

                def get_relationship(self, instance=instance, key=key,
                                     association_table=association_table):
                    instance_model = get_model(self, instance.model)
                    instance_table_name = instance_model.__tablename__
                    return sqla_orm.relationship(
                        instance.model,
                        secondary=association_table or sqla.Table(
                            f'{self.__tablename__}_{key}',
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
                                name=f'{self.__tablename__}_{key}_assoc_pk'
                            )
                        ),
                        **instance.extra
                    )

                if not is_abstract:
                    model = get_model(cls, instance.model)
                    secondary = f'{cls.__tablename__}_{key}'
                    attr_name = instance.extra.pop('backref', cls.__tablename__)
                    setattr(
                        model,
                        attr_name,
                        sqla_orm.relationship(cls, secondary=secondary)
                    )

                new_attrs[key] = declarative.declared_attr(get_relationship)

            elif isinstance(instance, relationships.ForeignKey):

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

            elif isinstance(instance, fields.Field):
                new_attrs[key] = sqla.Column(
                    instance.column_class(*instance.args),
                    **instance.kwargs
                )

        for key, instance in new_attrs.items():
            dict_[key] = instance
            setattr(cls, key, dict_[key])

        super(XerionMeta, cls).__init__(classname, bases, dict_)
