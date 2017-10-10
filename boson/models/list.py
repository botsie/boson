#!/usr/bin/env python3

from boson.database import DB
from boson.models.sql_table import SQLTable

from pprint import pprint as pp


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
        tx = DB().session.begin_transaction()
        for value in self.values:
            self._add_node(tx, value)
        DB().session.commit_transaction()

    def hierarchy(self):
        tx = DB().session.begin_transaction()
        for list_item, list_item_children in self.values.items():
            self._set_parent(tx, None, list_item, list_item_children)
        DB().session.commit_transaction()

    def _add_node(self, tx, value):
        # XXX: Will need to handle relationships
        value_str = ""
        for key in value.keys():
            value_str = f"{value_str}{key}:${key} ,"
        value_str = value_str[:-1]  # trim trailing comma
        tx.run(f"MERGE (a:{self.name} {{" + value_str + "})", value)

    def _set_parent(self, tx, parent, item, children):
        pp("---")
        pp(parent) if parent is not None else pp("")
        pp(item) if item is not None else pp("")
        pp(children) if children is not None else pp("")
        if parent is not None:
            cypher = '\n'.join((
                f"MATCH (item:{self.name} {{name: $item_name}}),",
                f"      (parent:{self.name} {{name: $parent_name}})",
                f"MERGE (item)-[:CHILD_OF]->(parent)"
            ))
            tx.run(cypher, item_name=item, parent_name=parent)
        if children is not None:
            for new_item, new_item_children in children.items():
                self._set_parent(tx, item, new_item, new_item_children)
        return
