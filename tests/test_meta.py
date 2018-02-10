from xerion.extensions import DataBase


def test_init(db: DataBase):
    class ValueModel(db.Model):
        __tablename__ = "value_model"
        id = db.IntField(primary_key=True)
        name = db.StrField(nullable=False)

    db.metadata.create_all()

    value_1 = ValueModel(name="value_1")
    value_2 = ValueModel(name="value_2")

    db.session.add(value_1)
    db.session.add(value_2)
    db.session.commit()


def test_foreign_key(db: DataBase):
    class ValueModel(db.Model):
        __tablename__ = "value_model"
        id = db.IntField(primary_key=True)
        name = db.StrField(nullable=False)

    class FooModel(db.Model):
        __tablename__ = "foo_model"
        id = db.IntField(primary_key=True)
        value = db.ForeignKey(ValueModel)

    db.metadata.create_all()

    value_1 = ValueModel(name="value_1")
    value_2 = ValueModel(name="value_2")

    db.session.add(value_1)
    db.session.add(value_2)

    foo_1 = FooModel(value=value_1)
    foo_2 = FooModel(value=value_2)

    db.session.add(foo_1)
    db.session.add(foo_2)
    db.session.commit()

    assert foo_1.value_id == value_1.id
    assert foo_2.value_id == value_2.id
