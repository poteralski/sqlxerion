SQLXerion
=========
[![Build Status](https://travis-ci.org/rstit/sqlxerion.svg?branch=master)](https://travis-ci.org/rstit/sqlxerion)

version number: 0.0.1

Overview
--------

Legendary SQL-alchemical code capable of turning your code into gold

Examples
--------
##### ForeignKey
SQLAlchemy code
```python

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer(), primary_key=True)

    articles_author = relationship(
        "Article", primaryjoin='User.id == Article.author_id',
        back_populates='author'
    )
    articles_moderator = relationship(
        "Article",
        primaryjoin='User.id == Article.moderator_id',
        back_populates='moderator'
    )


class Article(Base):
    __tablename__ = 'diseases'
    id = Column(Integer(), primary_key=True)

    author_id = Column(Integer, ForeignKey('users.id'))
    author = relationship(
        User,
        foreign_keys='[Article.author_id]',
        back_populates='articles_author'
    )

    moderator_id = Column(Integer, ForeignKey('users.id'))
    moderator = relationship(
        User,
        foreign_keys='[Article.moderator_id]',
        back_populates='articles_moderator'
    )

```

SQLXerion equivalent
```python
class User(Base):
    __tablename__ = 'users'
    id = IntField(primary_key=True)


class Article(Base):
    __tablename__ = 'diseases'
    id = IntField(primary_key=True)

    author = ForeignKey(User)
    moderator = ForeignKey(User)

```

##### ManyToMany
SQLAlchemy code
```python

article_moderators = db.Table(
    'article_moderators',
    db.Column('left_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('right_id', db.Integer, db.ForeignKey('articles.id'))
)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer(), primary_key=True)

    moderated_articles = relationship("Article",
                                      secondary='article_moderators')


class Article(Base):
    __tablename__ = 'articles'
    id = Column(Integer(), primary_key=True)

    moderators = relationship(User, secondary='article_moderators')

```

SQLXerion equivalent
```python
class User(Base):
    __tablename__ = 'users'
    id = IntField(primary_key=True)


class Article(Base):
    __tablename__ = 'articles'
    id = IntField(primary_key=True)

    moderators = ManyToMany(User)

```