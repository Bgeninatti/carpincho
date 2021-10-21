import os


def load_config():
    config = {
        "DEFAULT": {
            "db_path": os.environ.get("db_path"),
            "fetch_limit": os.environ.get("fetch_limit"),
        },
        "DISCORD": {
            "token": os.environ.get("token"),
            "channel": os.environ.get("channel"),
            "admin_channel": os.environ.get("admin_channel"),
            "role": os.environ.get("role"),
        },
        "EVENTOL": {
            "username": os.environ.get("username"),
            "password": os.environ.get("password")
        }
    }
    return config
