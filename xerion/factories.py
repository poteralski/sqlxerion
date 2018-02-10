from sqlalchemy import orm as sqla_orm
from sqlalchemy.ext import declarative
import sqlalchemy as sqla
from .utils import get_model


def fields_factory(column_class, args, kwargs):
    return sqla.Column(column_class(*args), **kwargs)


def assoc_table_factory(self, instance_table_name, tablename, attr_name):
    """
    This method should be responsible for creating association tables
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


def many_to_many_factory(cls, instance, is_abstract, attr_name):
    """
    This method should be responsible for creating required M2M Objects
    """
    secondary = instance.extra.pop('secondary', None)
    secondary_tablename = f'{cls.__tablename__}_{attr_name}'

    def get_relationship(self, instance=instance, secondary=secondary):
        instance_model = get_model(self, instance.model)
        instance_table_name = instance_model.__tablename__
        if not secondary:
            secondary = assoc_table_factory(self,
                                            instance_table_name,
                                            secondary_tablename,
                                            attr_name)
        return sqla_orm.relationship(
            instance.model,
            secondary=secondary,
            **instance.extra
        )

    if not is_abstract:
        # create backref if is not abstract
        setattr(
            get_model(cls, instance.model),
            instance.extra.pop('backref', cls.__tablename__),
            sqla_orm.relationship(cls, secondary=secondary_tablename)
        )
    return declarative.declared_attr(get_relationship)


def foreign_key_factory(model, attr_name, new_attrs, nullable, primary_key, extra):
    new_attrs[f'{attr_name}_id'] = declarative.declared_attr(
        lambda self, model=model, nullable=nullable, primary_key=primary_key:
        sqla.Column(
            sqla.Integer,
            sqla.ForeignKey(f'{get_model(self, model).__tablename__}.id'),
            nullable=nullable,
            primary_key=primary_key
        )
    )
    new_attrs[attr_name] = declarative.declared_attr(
        lambda self, model=model, extra=extra:
        sqla_orm.relationship(
            model,
            **extra
        )
    )
