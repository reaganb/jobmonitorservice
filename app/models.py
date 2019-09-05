from config import ma, db, get_timestamp



class Modulelog(db.Model):
    __tablename__ = 'modulelog'
    __table_args__ = {'schema': 'modulelog'}
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.String, unique=True)
    app_name = db.Column(db.String)
    state = db.Column(db.String)
    timestamp = db.Column(db.String, default=get_timestamp())


class ModulelogSchema(ma.ModelSchema):
    class Meta:
        model = Modulelog
        sqla_session = db.session



