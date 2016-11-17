import os

from config import local_storage_path, db_path

__version__ = '1.0'

if not os.path.exists(local_storage_path):
    os.makedirs(local_storage_path)

if not os.path.exists(db_path):
    os.makedirs(local_storage_path)
