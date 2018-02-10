from sqlalchemy.ext import declarative
from sqlalchemy import orm as sqla_orm
from . import fields, relationships, utils, factories


class XerionMeta(declarative.DeclarativeMeta):
    def __init__(cls, classname, bases, dict_):
        is_abstract = dict_.get('__abstract__', False)
        new_attrs = cls.create_from_base(dict_, is_abstract)
        for key, instance in new_attrs.items():
            dict_[key] = instance
            setattr(cls, key, dict_[key])
        super(XerionMeta, cls).__init__(classname, bases, dict_)

    def create_from_base(cls, attr_dict, is_abstract):
        new_attrs = dict()

        for attr_name, instance in attr_dict.items():

            if isinstance(instance, relationships.ManyToMany):
                secondary_tablename = f'{cls.__tablename__}_{attr_name}'

                if not is_abstract:
                    # create backref if is not abstract
                    setattr(
                        utils.get_model(cls, instance.model),
                        instance.extra.pop('backref', cls.__tablename__),
                        sqla_orm.relationship(cls, secondary=secondary_tablename)
                    )

                new_attrs[attr_name] = factories.many_to_many_factory(
                    cls,
                    instance,
                    instance.extra.pop('secondary', None),
                    secondary_tablename,
                    is_abstract,
                    attr_name
                )

            elif isinstance(instance, relationships.ForeignKey):
                new_attrs[attr_name] = factories.foreign_key_rel_factory(
                    instance.model,
                    instance.nullable, instance.primary_key,
                    instance.extra
                )
                new_attrs[f'{attr_name}_id'] = factories.foreign_key_column_factory(
                    instance.model,
                    instance.nullable, instance.primary_key,
                    instance.extra
                )

            elif isinstance(instance, fields.Field):
                new_attrs[attr_name] = factories.fields_factory(
                    instance.column_class,
                    instance.args,
                    instance.kwargs
                )

        return new_attrs
