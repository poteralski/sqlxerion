from tests.base import BaseTestCase
from xerion import model, fields, relations


class TwoForeignKeyTestCase(BaseTestCase):
    def init_models(self):
        class User(model.BaseModel):
            __tablename__ = 'users'
            id = fields.IntField(primary_key=True)

        class Article(model.BaseModel):
            __tablename__ = 'articles'
            id = fields.IntField(primary_key=True)

            author = relations.ForeignKey(User)
            moderator = relations.ForeignKey(User)

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
