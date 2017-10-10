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
from pprint import pprint as pp

from sqlalchemy import inspect, create_engine, Table, Column, Integer, String, Numeric, MetaData, ForeignKey, Sequence, Date, text
from sqlalchemy.sql import table, column, select, update, insert


from boson.database import DB
import boson.models.list


class DropAll(object):
    """Drops all nodes and edges in the database"""

    def __init__(self, definition):
        self._definition = definition

    def execute(self):
        DB().session.run('MATCH (n) DETACH DELETE n')


class CreateList(object):
    """ Understands how to instantiate a list """

    def __init__(self, definition):
        self._definition = definition

    def execute(self):
        the_list = boson.models.list.List(self._definition)
        the_list.create()


class UpdateList(object):
    """ Understands how to update a list """

    def __init__(self, definition):
        self._definition = definition

    def execute(self):
        the_list = boson.models.list.List(self._definition)
        the_list.populate()


class UpdateListHierarchy(object):
    """Understands how to add a hierarchy to a list"""

    def __init__(self, definition):
        self._definition = definition

    def execute(self):
        the_list = boson.models.list.List(self._definition)
        the_list.hierarchy()  # TODO: Pass the hierarchy as a parameter


class CreateTransaction(object):
    """ Understands how to create a transaction type """

    def __init__(self, definition):
        self._definition = definition

    def execute(self):
        pass


class UpdateTransaction(object):
    """ Understands how to update a transaction """

    def __init__(self, definition):
        self._definition = definition

    def execute(self):
        the_transaction = boson.models.list.Transaction(self._definition)
        the_transaction.populate()
