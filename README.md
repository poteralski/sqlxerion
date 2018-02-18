# SQLXerion

> Philosopher’s stone (xerion) they are looking for by all (SQL) alchemists
That hypothetical library they believed could convert some code into gold.
Now, this is available in PyPI.

## Installation

```bash
$ pip install SQLXerion
```

## Usage

First of all, you need to initialize SQLXerion extension.

```python
from xerion.extensions import DataBase

class App(NamedTuple):
    config: dict

app = App(config={'SQLALCHEMY_DATABASE_URI': 'sqlite://'})
db = DataBase()
db.init_app(app)
```

Then create your models:

```python
class ValueModel(db.Model):
    __tablename__ = "value_model"
    id = db.IntField(primary_key=True)
    name = db.StrField(nullable=False)
```

## Features

##### ForeignKey

```python
class ValueModel(db.Model):
    __tablename__ = "values"
    id = db.IntField(primary_key=True)
    name = db.StrField(nullable=False)

class FooModel(db.Model):
    __tablename__ = "foos"
    id = db.IntField(primary_key=True)
    value = db.ForeignKey(ValueModel)
```

is equal to:

```python
class ValueModel(Base):
    __tablename__ = "values"
    id = Column(Integer, primary_key=True)
    value = Column(String)
    foos = relationship("FooModel")

class FooModel(db.Model):
    __tablename__ = "foos"
    id = Column(Integer, primary_key=True)
    value_id = Column(Integer, ForeignKey('values.id'))
    value = relationship(ValueModel)
```

##### ManyToMany

```python
class ValueModel(db.Model):
    __tablename__ = "values"
    id = db.IntField(primary_key=True)
    name = db.StrField(nullable=False)

class FooModel(db.Model):
    __tablename__ = "foos"
    id = db.IntField(primary_key=True)
    values = db.ManyToMany(ValueModel)
```

is equal to:
```python
class ValueModel(Base):
    __tablename__ = "values"
    id = Column(Integer, primary_key=True)
    value = Column(String)
    foos = relationship("FooModel", secondary="foos_values_assoc")

class FooModel(db.Model):
    foos_values = Table(
        "foos_values_assoc",
        Column('left_id', Integer, ForeignKey(f'foos.id')),
        Column('right_id', Integer, ForeignKey(f'values.id'))
    )
    __tablename__ = "foos"
    id = db.IntField(primary_key=True)
    values = relationship(ValueModel, secondary="foos_values_assoc")
```

