from sqlxerion.extension import DataBase

db = DataBase()


class Person(db.Model):
    __tablename__ = 'persons'
    id = db.IntField(primary_key=True)


class Address(db.Model):
    __tablename__ = 'addresses'
    id = db.IntField(primary_key=True)

    person = db.ForeignKey(Person)