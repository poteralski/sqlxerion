from collections import namedtuple
from unittest import TestCase

from examples.profile import models


class OneForeignKeyTestCase(TestCase):
    def setUp(self):
        app = namedtuple("App", ['config'])({"SQLALCHEMY_DATABASE_URI": 'sqlite:///:memory:'})
        models.db.init_app(app)
        models.db.metadata.create_all()
        self.create_entities()

    def create_entities(self):
        self.person = models.Person()
        self.address = models.Address()

        self.address.person = self.person

        models.db.session.add(self.address)
        models.db.session.commit()

    def test_relation_created(self):
        assert self.address.person == self.person

    def test_column_created(self):
        assert self.address.person_id == self.person.id

    def test_backref_created(self):
        assert self.person.adresses == [self.address]
