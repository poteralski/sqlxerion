from unittest import TestCase
from sqlalchemy import orm, create_engine

from xerion import model, fields, relations


class BaseTestCase(TestCase):
    def prepare_session(self):
        self.engine = create_engine('sqlite:///:memory:', echo=False)
        self.session_maker = orm.sessionmaker(bind=self.engine)
        self.session = orm.scoped_session(self.session_maker)

    def prepare_models(self):
        pass

    def create_models(self):
        model.BaseModel.metadata.drop_all(self.engine)
        model.BaseModel.metadata.create_all(self.engine)

    def setUp(self):
        self.prepare_session()
        self.prepare_models()
        self.create_models()

    def tearDown(self):
        model.BaseModel.metadata.drop_all(self.engine)


class ForeignKeyTestCase(BaseTestCase):
    def prepare_models(self):
        class User(model.BaseModel):
            __tablename__ = 'users'
            id = fields.IntField(primary_key=True)

        class Article(model.BaseModel):
            __tablename__ = 'articles'
            id = fields.IntField(primary_key=True)

            author = relations.ForeignKey(User)

        self.User = User
        self.Article = Article

    def test_column_id_created(self):
        u = self.User()

        a = self.Article()
        a.author = u

        self.session.add(a)
        self.session.commit()

        assert a.author == u
        assert a.author_id == u.id

        assert a.author == u
        assert a.author_id == u.id

    def test_backref_created(self):
        u = self.User()

        a = self.Article()
        a.author = u

        self.session.add(a)
        self.session.commit()

        assert u.articles == [a]
