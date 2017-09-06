from unittest import TestCase

from sqlalchemy import create_engine, orm

from xerion import metadata


class BaseTestCase(TestCase):
    def init_models(self):
        pass

    def init_orm(self):
        self.engine = create_engine('sqlite:///:memory:', echo=False)
        self.session_maker = orm.sessionmaker(bind=self.engine)
        self.session = orm.scoped_session(self.session_maker)
        metadata.clear()

    def create_models(self):
        metadata.drop_all(self.engine)
        metadata.create_all(self.engine)

    def setUp(self):
        self.init_orm()
        self.init_models()
        self.create_models()

    def tearDown(self):
        metadata.drop_all(self.engine)
        metadata.clear()