#!/usr/bin/env python3

import sys
from pprint import pprint as pp

import inflect
from sqlalchemy import MetaData, Table, Column, ForeignKey, String, Integer, Numeric, text
from sqlalchemy.sql import table, column, select, update, insert


from boson.database import DB


class SQLTable(object):
    """ Understands how to manage the underlying RDBMS """

    def __init__(self, definition=None):
        if definition is not None:
            for k, v in definition.items():
                setattr(self, k, v)
        self._metadata = MetaData(bind=DB().engine)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self.table_name = value + '_table'
        self.view_name = value
        self._name = value

    def create(self):
        metadata = MetaData()
        table = Table(
            self.table_name,
            metadata,
            *self._columns()
        )
        metadata.create_all(DB().engine)
        self._mytable = table

        DB().engine.execute(
            text(f"CREATE VIEW {self.view_name} AS SELECT * FROM {self.table_name}"))

    def populate(self):
        self._mytable = Table(self.table_name, self._metadata, autoload=True)
        for value in self.values:
            s = self._mytable.select().where(
                self._mytable.c.name == value['name'])
            result = DB().connection.execute(s)
            value_exists = False
            for row in result:
                value_exists = True
            self._update(value) if value_exists else self._insert(value)

    def hierarchy(self):
        self._mytable = Table(self.table_name, self._metadata, autoload=True)
        for list_item, list_item_children in self.values.items():
            self._set_parent(None, list_item, list_item_children)

    def _set_parent(self, parent_item, list_item, list_item_chlidren):
        mytable = self._mytable
        if parent_item is not None:
            subselect = select([mytable.c[self._primary_key_name()]]).where(
                mytable.c.name == parent_item)
            s = mytable.update().\
                where(mytable.c.name == list_item).values(parent_id=subselect)
            DB().connection.execute(s)
        if list_item_chlidren is not None:
            for new_list_item, new_list_item_children in list_item_chlidren.items():
                self._set_parent(list_item, new_list_item,
                                 new_list_item_children)
        return

    def _update(self, value):
        s = update(self._mytable).\
            where(self._mytable.c.name == value['name']).\
            values(value)
        DB().connection.execute(s)

    def _insert(self, value):
        s = self._mytable.insert().values(value)
        DB().connection.execute(s)

    def _columns(self):
        columns = list()
        for c in self.attributes:
            columns.append(Column(c['name'], getattr(
                sys.modules[__name__], c['type'].replace('-', '_').capitalize())))
        # columns.insert(0,Column('name', String))
        columns.insert(0, Column(self._primary_key_name(),
                                 Integer, primary_key=True))
        columns.insert(0, Column('parent_id', Integer, ForeignKey(
            self.table_name + '.' + self._primary_key_name()), nullable=True))
        return columns

    def _primary_key_name(self):
        p = inflect.engine()
        return p.singular_noun(self.name) + '_id'
