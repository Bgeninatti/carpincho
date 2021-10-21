import json
import datetime
from enum import Enum

from peewee import (CharField, DateTimeField, Model, PrimaryKeyField, IntegerField, PostgresqlDatabase, TextField)

from carpincho.config import load_config

cfg = load_config()
database = PostgresqlDatabase(**cfg['DB'])


class BaseModel(Model):

    class Meta:
        database = database


class RegistrationStatus(Enum):
    PENDING = 0
    OK = 1
    NOT_FOUND = 2
    ALREADY_REGISTERED = 3


class Attendee(BaseModel):

    _attrs_mapping = {
        'nombre': 'id_first_name',
        'apellido': 'id_last_name',
        'sobrenombre': 'id_nickname',
        'email': 'id_email',
        'ticket': 'id_ticket',
        'meta': 'id_customFields'
    }

    id = PrimaryKeyField()
    attendee_id = IntegerField(unique=True)
    nombre = CharField(null=True)
    apellido = CharField(null=True)
    sobrenombre = CharField(null=True)
    discord_user = CharField(null=True)
    email = CharField()
    ticket = CharField()
    meta = TextField()
    status = CharField(default=RegistrationStatus.PENDING.name)
    created = DateTimeField(default=datetime.datetime.now)
    updated = DateTimeField(default=datetime.datetime.now)

    class Meta:
        order_by = ['-id']

    @classmethod
    def from_html(cls, soup, **kwargs):
        for name, _id in cls._attrs_mapping.items():
            if name == 'meta':
                kwargs[name] = json.loads(soup.find('textarea', id=_id).text)
            elif name == 'ticket':
                kwargs[name] = soup.find('select', id=_id).find('option', selected=True).text
            else:
                kwargs[name] = soup.find('input', id=_id).get('value')
        return cls(**kwargs)


def init_db():
    database.init(cfg['DB']['database'])
    database.connect()
    database.create_tables([Attendee])
    return database
