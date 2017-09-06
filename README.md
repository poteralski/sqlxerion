SQLXerion
=========
[![Build Status](https://travis-ci.org/rstit/sqlxerion.svg?branch=master)](https://travis-ci.org/rstit/sqlxerion)

version number: 0.0.1

Overview
--------

Legendary SQL-alchemical code capable of turning your code into gold

Examples
--------

SQLAlchemy code
```python

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer(), primary_key=True)

    articles_author = relationship("Article", primaryjoin='User.id == Article.author_id', back_populates='author')
    articles_moderator = relationship("Article", primaryjoin='User.id == Article.moderator_id', back_populates='moderator')


class Article(Base):
    __tablename__ = 'diseases'
    id = Column(Integer(), primary_key=True)

    author_id = Column(Integer, ForeignKey('users.id'))
    author = relationship(User, foreign_keys='[Article.author_id]', back_populates='articles_author')

    moderator_id = Column(Integer, ForeignKey('users.id'))
    moderator = relationship(User, foreign_keys='[Article.moderator_id]', back_populates='articles_moderator')

```

SQLXerion code
```python

```