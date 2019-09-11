import tempfile
import hashlib
import os.path as op
import os
import shutil
from sqlalchemy import or_
from magic import Magic, MagicException
from flask import make_response, abort
from sqlalchemy.exc import DataError, IntegrityError
from fileupload.models import FileMetadata, FileMetadataSchema, db

f = Magic(mime=True)

BASE_DIR = op.dirname(__file__)


#
def upload_file(upfile):
    metadata = extract_meta(upfile)

    schema = FileMetadataSchema()
    new_file = FileMetadata(
        size=metadata['file_size'],
        file_name=metadata['file_name'],
        sha1=metadata['file_sha1'],
        md5=metadata['file_md5'],
        type=metadata['file_type'],
    )

    try:
        db.session.add(new_file)
        db.session.commit()
        data = schema.dump(new_file)
        data.pop('id')
        save_to_host(new_file.id, upfile)

        return make_response(data, 201)
    except DataError as e:
        print(e)
        db.session.rollback()
        db.session.commit()
        return abort(403, "File already exist!")
    except IntegrityError as e:
        print(e)
        db.session.rollback()
        db.session.commit()
        return abort(403, "File already exist!")

#
def read_files():

        all_files = (
            FileMetadata.query.all()
        )

        schema = FileMetadataSchema()

        def remove_id(dct):
            d = schema.dump(dct)
            d.pop('id')
            return d

        data = [remove_id(af) for af in all_files]

        return data

#
def read_file(hash):
    print(hash)
    file = FileMetadata.query.filter(or_(FileMetadata.md5 == hash, FileMetadata.sha1 == hash)).one_or_none()

    if file:
        schema = FileMetadataSchema()
        data = schema.dump(file)

        data.pop('id')

        return data
    else:
        abort(
            404,
            "File not found!"
        )

#
def update_file(hash, file):

    update_file = FileMetadata.query.filter(or_(FileMetadata.md5 == hash, FileMetadata.sha1 == hash)).one_or_none()

    if update_file:

        if file['file_name']:
            rename_file_in_host(update_file.id, update_file.file_name, file['file_name'])

        schema = FileMetadataSchema()
        update = schema.load(file, session=db.session, instance=update_file)

        update.id = update_file.id

        db.session.merge(update)
        db.session.commit()

        data = schema.dump(update)

        data.pop('id')
        return data

    else:
        abort(
            404,
            "File not found!"
        )

def delete_file(hash):

    file = FileMetadata.query.filter(or_(FileMetadata.md5 == hash, FileMetadata.sha1 == hash)).one_or_none()

    if file:
        print(file.id)

        db.session.delete(file)
        db.session.commit()

        delete_file_in_host(file.id)

        return make_response("File deleted!", 201)

def save_to_host(file_id, file):
    print(BASE_DIR)
    dir_path = op.join(BASE_DIR, "files", str(file_id))
    os.mkdir(dir_path)
    file_path = op.join(dir_path, file.filename)
    file.save(file_path)

def delete_file_in_host(id):
    delete_id = str(id)
    dir_path = op.join(BASE_DIR, "files", delete_id)

    if op.isdir(dir_path):
        print(dir_path)
        shutil.rmtree(dir_path)

def rename_file_in_host(id, old_fname, new_fname):
    rename_id = str(id)
    dir_path = op.join(BASE_DIR, "files", rename_id)
    file_path_old = op.join(dir_path, old_fname)
    file_path_new = op.join(dir_path, new_fname)
    print(file_path_old)
    print(file_path_new)

    if op.isdir(dir_path) and op.isfile(file_path_old):
        os.rename(file_path_old, file_path_new)


def extract_meta(upfile):
    with tempfile.TemporaryDirectory() as tmp:
        file_name = upfile.filename

        temp_file = op.join(tmp, file_name)
        upfile.save(temp_file)

        file_size = op.getsize(temp_file)
        file_type = extract_file_type(temp_file)
        file_md5 = hash_file(temp_file, algorithm="md5")
        file_sha1 = hash_file(temp_file)

        return {
            "file_size": file_size,
            "file_name": file_name,
            "file_sha1": file_sha1,
            "file_md5": file_md5,
            "file_type": file_type
        }


def extract_file_type(file):
    try:
        return f.from_file(file)
    except MagicException:
        return None


def hash_file(file, algorithm='sha1'):
    """The method for computing the checksum hashing of the file depending on the algorithm provided

    Keyword arguments:
    file -- the directory path for recursive listing
    algorithm -- the algorithm to use (default 'md5')
    """

    block_size = 65536
    if algorithm == 'sha1':
        hasher = hashlib.sha1()
    else:
        hasher = hashlib.md5()

    with open(file, 'rb') as hash_file:
        buf = hash_file.read(block_size)
        while len(buf) > 0:
            hasher.update(buf)
            buf = hash_file.read(block_size)

    return hasher.hexdigest()







