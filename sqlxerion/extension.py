import sqlalchemy

from . import fields, model, relations


class DataBase:
    _session = None

    def __init__(self) -> None:
        self.metadata = sqlalchemy.MetaData()

        self.Model = model.xerion_base(self.metadata)

        self.ForeignKey = relations.ForeignKey
        self.ManyToMany = relations.ManyToMany

        self.BoolField = fields.BoolField
        self.IntField = fields.IntField
        self.StrField = fields.StrField
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
        self.engine = sqlalchemy.create_engine(uri, echo=True)
        self.session_maker = sqlalchemy.orm.sessionmaker(bind=self.engine)
        self._session = sqlalchemy.orm.scoped_session(self.session_maker)
        self.metadata.bind = self.engine

    def close_session(self):
        self.session.close_all()
