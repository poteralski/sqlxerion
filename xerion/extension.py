import sqlalchemy

from . import fields, metadata, model, relations


class DataBase:
    _session = None

    def __init__(self) -> None:
        self.metadata = metadata
        self.Model = model.BaseModel
        self.ForeignKey = relations.ForeignKey
        self.ManyToMany = relations.ManyToMany
        self.BoolField = fields.BoolField
        self.IntField = fields.IntField
        self.StrField = fields.StrField
        self.ChoiceField = fields.ChoiceField
        self.FloatField = fields.FloatField
        self._password_schemes = ''
        self._password_depr_schemes = ''

    def init_app(self, app):
        uri = app.config['SQLALCHEMY_DATABASE_URI']
        self._create_session(uri=uri)

    @property
    def session(self):
        if not self._session:
            raise RuntimeError("Session requires initialization.")
        return self._session

    def _create_session(self, uri):
        engine = sqlalchemy.create_engine(uri)
        self._session = sqlalchemy.orm.session.sessionmaker(bind=engine)()
        self.metadata.bind = engine

    def close_session(self):
        self.session.close_all()
