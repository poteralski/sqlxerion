from sqlalchemy.ext import declarative

from xerion.factories import many_to_many_factory, foreign_key_factory, \
    fields_factory
from . import fields, relationships


def create_from_base(cls, attr_dict, is_abstract):
    new_attrs = dict()

    for attr_name, instance in attr_dict.items():
        if isinstance(instance, relationships.ManyToMany):
            new_attrs[attr_name] = many_to_many_factory(cls, instance, is_abstract, attr_name)

        elif isinstance(instance, relationships.ForeignKey):
            foreign_key_factory(instance, attr_name, new_attrs)

        elif isinstance(instance, fields.Field):
            new_attrs[attr_name] = fields_factory(instance)

    return new_attrs


class XerionMeta(declarative.DeclarativeMeta):
    def __init__(cls, classname, bases, dict_):
        is_abstract = dict_.get('__abstract__', False)
        new_attrs = create_from_base(cls, dict_, is_abstract)
        for key, instance in new_attrs.items():
            dict_[key] = instance
            setattr(cls, key, dict_[key])
        super(XerionMeta, cls).__init__(classname, bases, dict_)
