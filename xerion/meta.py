from sqlalchemy.ext.declarative import DeclarativeMeta, declared_attr
from sqlalchemy import Column, Integer, Table, PrimaryKeyConstraint, \
    ForeignKey as FK, MetaData
from sqlalchemy.orm import relationship

from . import fields, relationships


class XerionMeta(DeclarativeMeta):
    def __init__(cls, classname, bases, dict_):
        new_attrs = dict()

        for key, instance in dict_.items():

            is_abstract = dict_.get('__abstract__', False)

            def get_model(self, model):
                if isinstance(model, str):
                    return self._decl_class_registry[model]
                else:
                    return model

            if isinstance(instance, relationships.ManyToMany):
                association_table = instance.extra.pop('secondary', None)

                def get_relationship(self, instance=instance, key=key,
                                     association_table=association_table):
                    instance_table_name = get_model(self, instance.model).__tablename__
                    return relationship(
                        instance.model,
                        secondary=association_table or Table(
                            f'{self.__tablename__}_{key}',
                            self.metadata,
                            Column('left_id', Integer, FK(f'{self.__tablename__}.id')),
                            Column('right_id', Integer,
                                   FK(f'{instance_table_name}.id')),
                            PrimaryKeyConstraint('left_id', 'right_id',
                                                 name=f'{self.__tablename__}_'
                                                      f'{key}'
                                                      f'_association_pk')
                        ),
                        **instance.extra
                    )

                # Problem with Many To Many auto backrefs relationship
                # https://stackoverflow.com/questions/45313491/

                if not is_abstract:
                    model = get_model(cls, instance.model)
                    secondary = f'{cls.__tablename__}_{key}'
                    attr_name = instance.extra.pop('backref', cls.__tablename__)
                    setattr(model, attr_name, relationship(cls, secondary=secondary))

                new_attrs[key] = declared_attr(get_relationship)

            elif isinstance(instance, relationships.ForeignKey):

                def get_column(self, instance=instance):
                    instance_table_name = get_model(self, instance.model).__tablename__
                    return Column(Integer, FK(f'{instance_table_name}.id'),
                                  nullable=instance.nullable, primary_key=instance.primary_key)

                new_attrs[f'{key}_id'] = declared_attr(get_column)
                new_attrs[key] = declared_attr(
                    lambda self, instance=instance: relationship(instance.model,
                                                                 **instance.extra))

            elif isinstance(instance, fields.Field):
                new_attrs[key] = Column(instance.column_class(*instance.args), **instance.kwargs)

        for key, instance in new_attrs.items():
            dict_[key] = instance
            setattr(cls, key, dict_[key])

        super(XerionMeta, cls).__init__(classname, bases, dict_)
