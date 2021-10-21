import os
from urllib.parse import urlparse


def load_config():
    params = urlparse(os.environ["DATABASE_URL"])
    config = {
        "DB": {
            "database": params.path[1:],
            "user": params.username,
            "password": params.password,
            "host": params.hostname,
            "port": params.port,
        },
        "DISCORD": {
            "token": os.environ.get("token"),
            "channel": os.environ.get("channel"),
            "admin_channel": os.environ.get("admin_channel"),
            "role": os.environ.get("role"),
        },
        "EVENTOL": {
            "username": os.environ.get("username"),
            "password": os.environ.get("password"),
            "fetch_limit": os.environ.get("fetch_limit"),
        }
    }
    return config
