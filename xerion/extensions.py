from sqlalchemy import create_engine, orm

from . import fields, metadata, model


class DataBase:
    _session = None

    @property
    def session(self):
        return self._session

    def __init__(self) -> None:
        self.metadata = metadata
        self.Model = model.BaseModel
        self.ForeignKey = fields.ForeignKey
        self.ManyToMany = fields.ManyToMany
        self.BoolField = fields.BoolField
        self.IntField = fields.IntField
        self.StrField = fields.StrField
        self.FloatField = fields.FloatField

    def init_app(self, app):
        self._create_session(app)

    def _create_session(self, app):
        self._engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
        self._session_factory = orm.sessionmaker(bind=self._engine, autoflush=False)
        self._session = self._session_factory()
        self.metadata.bind = self._engine
