from sqlxerion.extension import DataBase

db = DataBase()


class User(db.Model):
    __tablename__ = 'users'
    id = db.IntField(primary_key=True)


class Article(db.Model):
    __tablename__ = 'articles'
    id = db.IntField(primary_key=True)

    author = db.ForeignKey(User)
    moderator = db.ForeignKey(User)
