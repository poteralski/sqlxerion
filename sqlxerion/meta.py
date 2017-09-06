from sqlalchemy.ext.declarative import DeclarativeMeta, declared_attr
import sqlalchemy
from sqlalchemy.orm import relationship

from sqlxerion import fields, utils, relations


class PrimaMateria(DeclarativeMeta):
    def __init__(cls, classname, bases, dict_):
        new_attrs = dict()

        for key, instance in dict_.items():

            abstract = dict_.get('__abstract__', False)

            if isinstance(instance, relations.ManyToMany):
                association_table = instance.extra.pop('secondary', None)

                def get_relationship(self, instance=instance, association_table=association_table):
                    instance_table_name = utils.get_model(self, instance.model).__tablename__
                    return relationship(
                        instance.model,
                        secondary=association_table or sqlalchemy.Table(
                            f'{self.__tablename__}_{instance_table_name}',
                            instance.model.metadata,
                            sqlalchemy.Column(
                                'left_id',
                                sqlalchemy.Integer,
                                sqlalchemy.ForeignKey(f'{self.__tablename__}.id')
                            ),
                            sqlalchemy.Column(
                                'right_id',
                                sqlalchemy.Integer,
                                sqlalchemy.ForeignKey(f'{instance_table_name}.id')
                            ),
                            sqlalchemy.PrimaryKeyConstraint(
                                'left_id',
                                'right_id',
                                name=f'{self.__tablename__}_{instance_table_name}_association_pk')
                        ),
                        **instance.extra
                    )

                # Problem with Many To Many auto backrefs relationship
                # https://stackoverflow.com/questions/45313491/

                if not abstract:
                    model = utils.get_model(cls, instance.model)
                    secondary = f'{cls.__tablename__}_{model.__tablename__}'
                    attr_name = instance.extra.pop('backref', cls.__tablename__)
                    setattr(model, attr_name, relationship(cls, secondary=secondary))

                new_attrs[key] = declared_attr(get_relationship)

            elif isinstance(instance, relations.ForeignKey):

                def get_column(self, instance=instance):
                    instance_table_name = utils.get_model(self, instance.model).__tablename__
                    return sqlalchemy.Column(
                        sqlalchemy.Integer,
                        sqlalchemy.ForeignKey(f'{instance_table_name}.id'),
                        nullable=instance.nullable
                    )

                new_attrs[f'{key}_id'] = declared_attr(get_column)
                new_attrs[key] = declared_attr(lambda self, instance=instance: relationship(instance.model, **instance.extra))

            elif isinstance(instance, fields.Field):
                new_attrs[key] = sqlalchemy.Column(
                    instance.column_class(*instance.args),
                    **instance.kwargs
                )

        for key, instance in new_attrs.items():
            dict_[key] = instance
            setattr(cls, key, dict_[key])

        super(PrimaMateria, cls).__init__(classname, bases, dict_)

