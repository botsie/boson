#!/usr/bin/env python3

from boson.database import DB
# from boson.models.sql_table import SQLTable

from pprint import pprint as pp


class GraphNodeType(object):
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

        tx = DB().session.begin_transaction()
        for value in self.values:
            self._add_relationships(tx, value)
        DB().session.commit_transaction()

    def hierarchy(self):
        tx = DB().session.begin_transaction()
        for list_item, list_item_children in self.values.items():
            self._set_parent(tx, "", None, list_item, list_item_children)
        DB().session.commit_transaction()

    @property
    def labels(self):
        return ':' + self.name

    def _add_node(self, tx, value):
        # XXX: Will need to handle relationships
        value_str = ""
        for key in value.keys():
            value_str = f"{value_str}{key}:${key} ,"
        value_str = value_str[:-1]  # trim trailing comma

        tx.run(f"MERGE ({self.labels} {{" + value_str + "})", value)
        # self._add_relationships(tx, value)

    def _add_relationships(self, tx, value):
        for key, value in value.items():
            if key in DB().lists:
                cypher = " ".join((
                    f"MATCH (a{self.labels} {{{key}: ${key}}}),",
                    f"      (b:{key}:list {{name: ${key}}})",
                    f"MERGE (a)-[:REFERENCES]->(b)"
                ))
                tx.run(cypher, {key: value})

    def _set_parent(self, tx, ancestors, parent, item, children):
        path = ancestors + ':' + item
        if parent is not None:
            cypher = ' '.join((
                f"MATCH (item{self.labels} {{name: $item_name}}),",
                f"      (parent{self.labels} {{name: $parent_name}})",
                f"MERGE (item)-[:CHILD_OF]->(parent)"
            ))
            tx.run(cypher, item_name=item, parent_name=parent)

        cypher = ' '.join((
            f"MATCH (item{self.labels} {{name: $item_name}})",
            f"SET item.path = $path"
        ))
        tx.run(cypher, item_name=item, path=path)

        if children is not None:
            for new_item, new_item_children in children.items():
                self._set_parent(tx, path, item,
                                 new_item, new_item_children)
        return


class List(GraphNodeType):

    @property
    def labels(self):
        return ':' + self.name + ':list'


class Transaction(GraphNodeType):
    pass
