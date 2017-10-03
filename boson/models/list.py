#!/usr/bin/env python3

import sys

import inflect
from sqlalchemy import MetaData, Table, Column, ForeignKey, String, Integer, Numeric

from boson.database import DB

class List(object):
    """ Understands List CRUD operations """
    
    def __init__(self, definition):
        self._definition = definition
    
    def create(self):
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
        columns.insert(0,Column(self._primary_key_name(), Integer, primary_key=True))
        columns.insert(0,Column('parent_id', Integer, ForeignKey(self._definition['name'] + '.' + self._primary_key_name()), nullable=True))
        return columns

    def _primary_key_name(self):
        p = inflect.engine()
        return p.singular_noun(self._definition['name']) + '_id'


class Transaction(object):
    pass