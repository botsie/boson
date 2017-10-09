#!/usr/bin/env python3

from boson.models.sql_table import SQLTable


class List(object):
    def __init__(self, definition):
        # self._definition = definition
        if definition is not None:
            for k, v in definition.items():
                setattr(self, k, v)

    def create(self):
        s = SQLTable()
        s.name = self.name
        s.attributes = self.attributes
        s.attributes.insert(0, {'name': 'name', 'type': 'String'})
        s.create()

    def populate(self):
        s = SQLTable()
        s.name = self.name
        s.values = self.values
        s.populate()

    def hierarchy(self):
        s = SQLTable()
        s.name = self.name
        s.values = self.values
        s.hierarchy()
