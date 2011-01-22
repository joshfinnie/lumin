from decimal import Decimal

from pymongo.son_manipulator import SONManipulator

import colander

SENTINEL = {u'_type': u'colander.null'}

class ColanderNullTransformer(SONManipulator):
    """
    Added to the db at load time, this allows MongoDB to store and
    retrieve colander.null sentinals for unknown values. A
    :term:`son_manipulator` is a object that edits :term:`SON` objects
    as they enter or exit a MongoDB

    .. code-block:: python

       import pymongo
       db = pymongo.Connection().testdb['acollection']
       from lumin.son import ColanderNullTransformer
       db.add_son_manipulator(ColanderNullTransformer())
    """
    def transform_incoming(self, son, collection):
        """
        """
        for (k, v) in son.items():
            if v is colander.null:
                son[k] = SENTINEL
                continue
            if isinstance(v, dict):
                self.recursive_in(v)
        return son

    def transform_outgoing(self, son, collection):
        """
        """
        for (k, v) in son.items():
            if isinstance(v, dict):
                if v !=SENTINEL:
                    self.recursive_out(v)
                elif v == SENTINEL:
                    son[k] = colander.null
        return son

    def recursive_in(self, subson):
        """
        """
        for (k, v) in subson.items():
            if v is colander.null:
                subson[k] = SENTINEL
                continue
            if isinstance(v, dict):
                for (key, value) in v.items():
                    if value is colander.null:
                        v[key] = SENTINEL
                    if isinstance(value, dict):
                        self.recursive_in(value)

    def recursive_out(self, subson):
        """
        """
        for (k, v) in subson.items():
            if isinstance(v, dict):
                if v == SENTINEL:
                    subson[k] = colander.null
                self.recursive_out(v)


class DecimalTransformer(SONManipulator):
    """
    """
    def transform_incoming(self, son, collection):
        """
        """
        for (k, v) in son.items():
            if isinstance(v, Decimal):
                son[k] = {'_type' : 'decimal', 'value' : unicode(v)}
            elif isinstance(v, dict):
                son[k] = self.transform_incoming(v, collection)
        return son

    def transform_outgoing(self, son, collection):
        """
        """
        for (k, v) in son.items():
            if isinstance(v, dict):
                if "_type" in v and v["_type"] == "decimal":
                   son[k] = Decimal(v['value'])
                else:
                   son[k] = self.transform_outgoing(v, collection)
        return son


class DeNull:
    """
    """
    def __call__(self, son):
        """
        """
        return self.transform(son)

    def transform(self, son):
        """
        """
        for (k, v) in son.items():
            if v is colander.null:
                son[k] = ''
                continue
            if isinstance(v, dict):
                self.recurse(v)
        return son

    def recurse(self, subson):
        """
        """
        for (k, v) in subson.items():
            if v is colander.null:
                subson[k] = ''
                continue
            if isinstance(v, dict):
                for (key, value) in v.items():
                    if value is colander.null:
                        v[key] = ''
                    if isinstance(value, dict):
                        self.recurse(value)
denull = DeNull()


class DeSentinel:
    """
    """
    def __call__(self, son):
        """
        """
        return self.transform(son)

    def transform(self, son):
        """
        """
        for (k, v) in son.items():
            if v is SENTINEL:
                son[k] = ''
                continue
            if isinstance(v, dict):
                self.recurse(v)
        return son

    def recurse(self, subson):
        """
        """
        for (k, v) in subson.items():
            if v is SENTINEL:
                subson[k] = ''
                continue
            if isinstance(v, dict):
                for (key, value) in v.items():
                    if value is SENTINEL:
                        v[key] = ''
                    if isinstance(value, dict):
                        self.recurse(value)
desentinel = DeSentinel()
