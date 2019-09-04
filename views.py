from flask import make_response, abort
from app.models import Modulelog, ModulelogSchema
from config import get_timestamp, db


JOBS = {
    "a1": {
        "job_id": "a1",
        "app_name": "app1",
        "state": "STARTED",
        "timestamp": get_timestamp(),
    },
    "a2": {
        "job_id": "a2",
        "app_name": "app2",
        "state": "FINISHED",
        "timestamp": get_timestamp(),
    },
    "a3": {
        "job_id": "a3",
        "app_name": "app3",
        "state": "ERROR",
        "timestamp": get_timestamp(),
    },

}

def create_job(job):

    # app_name = job_id.get("app_name",None)
    state = job.get("state", None)
    app_name = job.get("app_name", None)
    job_id = job.get("job_id", None)

    existing_job = (
        Modulelog.query.filter(Modulelog.job_id == job_id)
        .one_or_none()
    )
    print(type(existing_job))

    if existing_job is None:
        print("Not exist!")
        schema = ModulelogSchema()
        new_job = Modulelog(job_id=job_id, state=state, app_name=app_name)

        db.session.add(new_job)
        db.session.commit()

        data = schema.dump(new_job)

        return data, 201
    else:
        abort(
            406,
            f"Job {job_id} already exists!"
        )

def read_job_all():
    all_jobs = (
        Modulelog.query.all()
    )
    schema = ModulelogSchema()

    data = []
    for aj in all_jobs:
        data.append(schema.dump(aj))

    return data

def read_job(job_id):

    job = Modulelog.query.filter(Modulelog.job_id == job_id).one_or_none()

    if job:
        schema = ModulelogSchema()
        data = schema.dump(job)
        return data
    else:
        abort(
            404,
            f"Job {job_id} not found!"
        )

def update_job(job_id, job):
    update_job = Modulelog.query.filter(
        Modulelog.job_id == job_id
    ).one_or_none()

    data = {}
    if update_job:
        schema = ModulelogSchema()
        update = schema.load(job, session=db.session).data

        update.job_id = update_job.job_id

        db.session.merge(update)
        db.session.commit()

        data = schema.dump(update_job).data

        return data, 200

def delete_job(job_id):
    job = Modulelog.query.filter(Modulelog.job_id == job_id).one_or_none()

    if job:
        db.session.delete(job)
        db.session.commit()
        return make_response(f"Job {job_id} deleted", 200)
    else:
        abort(404, f"Job not found for Id: {job_id}")




