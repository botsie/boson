#!/usr/bin/env python3

from boson.database import DB
from boson.models.sql_table import SQLTable


class List(object):
    def __init__(self, definition):
        # self._definition = definition
        if definition is not None:
            for k, v in definition.items():
                setattr(self, k, v)

    def create(self):
        pass
        # TODO: create list metadata here. No need to create a type in neo4j

    def populate(self):
        for record in self.values:
            DB().session.write_transaction(self._add_node, record)

    def hierarchy(self):
        s = SQLTable()
        s.name = self.name
        s.values = self.values
        s.hierarchy()

    def _add_node(self, tx, value):
        # XXX: Will need to handle relationships
        value_str = ""
        for key in value.keys():
            value_str = f"{value_str}{key}:${key} ,"
        value_str = value_str[:-1]  # trim trailing comma
        tx.run(f"MERGE (a:{self.name} {{" + value_str + "})", value)
