from flask import make_response, abort
from app.models import Modulelog, ModulelogSchema
from config import db
from sqlalchemy.exc import DataError


def create_job(job):

    state = job.get("state", None)
    app_name = job.get("app_name", None)

    schema = ModulelogSchema()
    new_job = Modulelog(state=state, app_name=app_name)

    try:
        db.session.add(new_job)
        db.session.commit()

        data = schema.dump(new_job)

        return data, 201
    except DataError:
        return abort(
            500,
            "Invalid value for the Job state!"
        )
        pass




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

    job = Modulelog.query.filter(Modulelog.job_id == job_id)

    if job:
        schema = ModulelogSchema()
        data = [schema.dump(j) for j in job]
        return data
    else:
        abort(
            404,
            f"Jobs for {job_id} not found!"
        )


def update_job(job_id, job):
    update_job = Modulelog.query.filter(
        Modulelog.id == job_id
    ).one_or_none()

    if update_job:
        print("exist")
        schema = ModulelogSchema()
        update = schema.load(job, session=db.session, instance=update_job)

        update.id = update_job.id

        db.session.merge(update)
        db.session.commit()

        data = schema.dump(update)

        return data, 200

def delete_job(job_id):
    job = Modulelog.query.filter(Modulelog.id == job_id).one_or_none()

    if job:
        db.session.delete(job)
        db.session.commit()
        return make_response(f"Job ID:{job_id} deleted!", 200)
    else:
        return  abort(404, f"Job ID:{job_id} not found!")




