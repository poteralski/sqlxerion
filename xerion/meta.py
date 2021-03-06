from sqlalchemy.ext import declarative
from . import fields, relationships, utils, factories


class XerionMeta(declarative.DeclarativeMeta):
    def __init__(cls, classname, bases, dict_):
        is_abstract = dict_.get('__abstract__', False)
        new_attrs = dict(cls.create_from_base(dict_, is_abstract))
        for key, instance in new_attrs.items():
            dict_[key] = instance
            setattr(cls, key, dict_[key])
        super(XerionMeta, cls).__init__(classname, bases, dict_)

    def create_from_base(cls, attr_dict, is_abstract):
        for attr_name, instance in attr_dict.items():
            secondary = None

            if isinstance(instance, relationships.ManyToMany):
                secondary = cls.resolve_secondary(attr_name, instance)
                yield attr_name, factories.many_to_many_factory(
                    instance,
                    secondary,
                    attr_name
                )
            elif isinstance(instance, relationships.ForeignKey):
                yield attr_name, factories.foreign_key_rel_factory(
                    instance.model,
                    instance.nullable, instance.primary_key,
                    instance.extra
                )
                yield f'{attr_name}_id', factories.foreign_key_column_factory(
                    instance.model,
                    instance.nullable, instance.primary_key,
                    instance.extra
                )

            elif isinstance(instance, fields.Field):
                yield attr_name, factories.fields_factory(
                    instance.column_class,
                    instance.args,
                    instance.kwargs
                )

            if not is_abstract and secondary is not None:
                # create backref if is not abstract
                # fix also for o2m
                setattr(
                    utils.get_model(cls, instance.model),
                    instance.extra.pop('backref', cls.__tablename__),
                    factories.relationship( cls, secondary=secondary)
                )

    def resolve_secondary(cls, attr_name, instance):
        return instance.extra.pop(
            'secondary',
            factories.assoc_table_factory(
                cls,
                utils.get_model(cls, instance.model).__tablename__,
                f'{cls.__tablename__}_{attr_name}',
                attr_name
            )
        )

