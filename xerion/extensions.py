from sqlalchemy import create_engine, orm, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from . import fields, meta, relationships


class DataBase:
    _session: Session = None

    @property
    def session(self) -> Session:
        return self._session

    def __init__(self, metadata=None) -> None:
        self.metadata = metadata or MetaData()
        self.Model = declarative_base(metaclass=meta.XerionMeta,
                                      metadata=self.metadata)
        self.ForeignKey = relationships.ForeignKey
        self.ManyToMany = relationships.ManyToMany
        self.BoolField = fields.BoolField
        self.IntField = fields.IntField
        self.StrField = fields.StrField
        self.FloatField = fields.FloatField

    def init_app(self, app):
        self._create_session(app)

    def _create_session(self, app):
        self._engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
        self._session_factory = orm.sessionmaker(bind=self._engine,
                                                 autoflush=False)
        self._session = self._session_factory()
        self.metadata.bind = self._engine
