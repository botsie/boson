#!/usr/bin/env python3

#
# Boson Task Classes
#

import yaml
import sys
import os
import logging
import inflect
import datetime

from sqlalchemy import inspect, create_engine, Table, Column, Integer, String, Numeric, MetaData, ForeignKey, Sequence, Date
from sqlalchemy.sql import table, column, select, update, insert

from pprint import pprint as pp

class DB(object):
    """ Singleton Encapsulation of the database connection """
    __instance = None

    def __new__(cls):
        if DB.__instance is None:
            DB.__instance = object.__new__(cls)
            with open('database.yml', 'r') as f:
                db_config = yaml.load(f)
            env = os.getenv('BOSON_ENV', 'development')
            connection_string = db_config[env]
            logging.debug("connecting to " + connection_string)
            DB.__instance.engine = create_engine(connection_string)
            DB.__instance.connection = DB.__instance.engine.connect()
        
        return DB.__instance

class CreateList(object):
    """ Understands how to instantiate a list """

    def __init__(self, definition):
        self._definition = definition

    def execute(self):
        metadata = MetaData()
        table = Table(
            self._definition['name'],
            metadata,
            *self._columns()
        )
        metadata.create_all(DB().engine)

    def _columns(self):
        columns = list()
        for c in self._definition['attributes']:
            columns.append(Column(c['name'], getattr(sys.modules[__name__], c['type'].replace('-','_').capitalize())))
        columns.insert(0,Column('name', String))
        columns.insert(0,Column(self._primary_key_name(), Integer, Sequence(self._definition['name'] + '_id_seq'), primary_key=True))
        return columns

    def _primary_key_name(self):
        p = inflect.engine()
        return p.singular_noun(self._definition['name']) + '_id'


class UpdateList(object):
    """ Understands how to update a list """

    def __init__(self, definition):
        self._definition = definition
        self._metadata = MetaData(bind=DB().engine)
        self._mytable = Table(self._definition['name'], self._metadata, autoload=True)

    def execute(self):
        for value in self._definition['values']:
            s = self._mytable.select().where(self._mytable.c.name==value['name'])
            result = DB().connection.execute(s)
            value_exists = False
            for row in result:
                value_exists = True
            self._update(value) if value_exists else self._insert(value)

    def _update(self, value):
        s = update(self._mytable).\
            where(self._mytable.c.name == value['name']).\
            values(value)
        DB().connection.execute(s)

    def _insert(self, value):
        s = self._mytable.insert().values(value)
        DB().connection.execute(s)

class CreateTransaction(object):
    """ Understands how to create a transaction type """

    def __init__(self, definition):
        self._definition = definition
        self._metadata = MetaData(bind=DB().engine)

    def execute(self):
        table = Table(
            self._definition['name'],
            self._metadata,
            *self._columns()
        )
        self._metadata.create_all(DB().engine)

    def _columns(self):
        columns = list()
        for c in self._definition['attributes']:
            logging.debug('column = ' + c['name'])
            if c['type'] == 'list':
                foreign_key = self._foreign_key(c['name']) 
                columns.append(Column(c['name'], Integer, ForeignKey(foreign_key), nullable=False))
            else:
                column_type = getattr(sys.modules[__name__], c['type'].replace('-','_').capitalize())
                columns.append(Column(c['name'], column_type))

        columns.insert(0,Column(self._primary_key_name(), Integer, Sequence(self._definition['name'] + '_id_seq'), primary_key=True))
        return columns

    def _primary_key_name(self):
        return self._definition['name'] + '_id'

    def _foreign_key(self, name):
        p = inflect.engine()
        t = Table(p.plural(name), self._metadata, autoload=True)
        return getattr(t.c, name + '_id')


class UpdateTransaction(object):
    """ Understands how to update a transaction """

    def __init__(self, definition):
        self._definition = definition
        self._metadata = MetaData(bind=DB().engine)
        self._mytable = Table(self._definition['name'], self._metadata, autoload=True)
        self._foreign_keys = self._get_foreign_keys()
        self._date_columns = self._get_date_columns()

    def execute(self):
        for value in self._definition['values']:
            if self._primary_key_name() in value.keys():
                self._update(value)
            else:
                self._insert(value)

    def _get_date_columns(self):
        inspector = inspect(DB().engine)
        date_colummns = []
        for col in inspector.get_columns(self._definition['name']):
            if isinstance(col['type'], Date):
                date_colummns.append(col['name'])
        return date_colummns
    
    def _get_foreign_keys(self):
        inspector = inspect(DB().engine)
        constrained_columns = {}
        for key in inspector.get_foreign_keys(self._definition['name']):
            # NOTE: I assume no composite foreign keys
            constrained_columns[key['constrained_columns'][0]] = {
                'referred_table': key['referred_table'],
                'referred_column': key['referred_columns'][0],
            }
        return constrained_columns

    def _primary_key_name(self):
        return self._definition['name'] + '_id'

    def _update(self, value):
        s = update(self._mytable).\
            where(self._mytable.c.name == value['name']).\
            values(value)
        DB().connection.execute(s)

    def _insert(self, value):
        the_values = {}
        for key, val in value.items():
            if key in self._foreign_keys.keys():
                referred_table_name = self._foreign_keys[key]['referred_table']
                referred_column = self._foreign_keys[key]['referred_column']
                referred_table = Table(referred_table_name, self._metadata, autoload=True)
                the_values[key] = select([referred_table.c[inflect.engine().singular_noun(referred_table_name) + '_id']]).\
                                    where(referred_table.c.name == val)
                                    # where(self._mytable.c[key] == referred_table.c[referred_column]).\
            elif key in self._date_columns:
                the_values[key] = datetime.datetime.strptime(val,'%Y/%m/%d') 
            else:
                the_values[key] = val 
        pp(the_values)
        s = self._mytable.insert().values(the_values)
        # logging.debug(str(s))
        DB().connection.execute(s)

