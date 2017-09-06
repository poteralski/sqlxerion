from collections import namedtuple
from unittest import TestCase

from examples.blog import models


class TwoForeignKeyTestCase(TestCase):
    def create_entities(self):
        self.user = models.User()
        self.article = models.Article()

        self.article.author = self.user

        models.db.session.add(self.article)
        models.db.session.commit()

    def setUp(self):
        app = namedtuple("App", ['config'])({"SQLALCHEMY_DATABASE_URI": 'sqlite:///:memory:'})
        models.db.init_app(app)
        models.db.metadata.create_all()
        self.create_entities()

    def test_column_id_created(self):
        assert self.article.author == self.user
        assert self.article.author_id == self.user.id

        assert self.article.author == self.user
        assert self.article.author_id == self.user.id

    def test_backref_created(self):
        assert self.user.articles == [self.article]
