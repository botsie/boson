#!/usr/bin/env python3

import yaml
import logging
import os
from pprint import pprint as pp

from neo4j.v1 import GraphDatabase


class DB(object):
    """ Singleton Encapsulation of the database connection """
    __instance = None

    def __new__(cls):
        if DB.__instance is None:
            DB.__instance = object.__new__(cls)
            env = os.getenv('BOSON_ENV', 'development')
            with open('database.yml', 'r') as f:
                conf = yaml.load(f)[env]
            logging.debug("connecting to " + conf['uri'])
            DB.__instance.driver = GraphDatabase.driver(
                conf['uri'], auth=(conf['user'], conf['password']))
            DB.__instance.session = DB.__instance.driver.session()

        return DB.__instance
