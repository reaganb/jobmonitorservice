from config import ma, db, get_timestamp
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

class Modulelog(db.Model):
    """
    The Modulelog table
    """
    __tablename__ = 'modulelog'
    __table_args__ = {'schema': 'modulelog'}
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(UUID(as_uuid=True), default=uuid4, index=True)
    app_name = db.Column(db.String, nullable=False)
    state = db.Column(db.Enum("STARTED", "FINISHED", "ERROR", name="job_states"), nullable=False)
    timestamp = db.Column(db.String, default=get_timestamp(), onupdate=get_timestamp())


class ModulelogSchema(ma.ModelSchema):
    """
    The schema for the module log table
    """
    class Meta:
        model = Modulelog
        sqla_session = db.session



