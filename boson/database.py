#!/usr/bin/env python3

import yaml
import logging
import os


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
