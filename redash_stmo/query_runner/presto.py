import collections
import logging

import six
from pyhive import presto
from redash.query_runner.presto import Presto
from redash.query_runner import register


logger = logging.getLogger(__name__)


class STMOPresto(Presto):
    """
    A custom Presto query runner. Currently empty.
    """


class STMOConnection(presto.Connection):
    """
    A custom Presto connection that uses the custom Presto cursor
    as the default cursor.
    """
    def cursor(self):
        return STMOPrestoCursor(*self._args, **self._kwargs)


class STMOPrestoCursor(presto.Cursor):
    """
    A custom Presto cursor that processes the data after it has been
    handled by the parent cursor to apply various transformations.
    """
    def _process_response(self, response):
        super(STMOPrestoCursor, self)._process_response(response)
        self._data = self._process_data()

    def _process_data(self):
        processed_data = collections.deque()
        for row in self._data:  # the top-level is an iterable of records (i.e. rows)
            item = []
            for column, row in zip(self._columns, row):
                item.append(self._format_data(column["typeSignature"], row))
            processed_data.append(item)
        return processed_data

    def _format_data(self, column, data):
        """Given a Presto column and its data, return a more human-readable
        format of its data for some data types."""
        type = column["rawType"]

        try:
            iter(data)  # check if the data is iterable
        except TypeError:
            return data  # non-iterables can simply be directly shown

        # records should have their fields associated with types
        # but keep the tuple format for backward-compatibility
        if type == "row":
            keys = column["literalArguments"]
            values = [
                self._format_data(c, d)
                for c, d in zip(column["typeArguments"], data)
            ]
            return tuple(zip(keys, values))

        # arrays should have their element types associated with each element
        elif type == "array":
            rep = [
                column["typeArguments"][0]
            ] * len(data)
            return [
                self._format_data(c, d)
                for c, d in zip(rep, data)
            ]

        # maps should have their value types associated with each value
        # (note that keys are always strings), but keep the tuple format
        # for backward-compatibility
        elif type == "map":
            value_type = column["typeArguments"][1]
            return [
                (k, self._format_data(value_type, v))
                for k, v in six.iteritems(data)
            ]

        else:
            # unknown type, don't process it
            return data


def stmo_connect(*args, **kwargs):
    """
    A custom connect function to be used to override the
    default pyhive.presto.connect function.
    """
    return STMOConnection(*args, **kwargs)


def extension(app):
    logger.info('Loading Redash Extension for the custom Presto query runner')
    # Monkeypatch the pyhive.presto.connect function
    presto.connect = stmo_connect
    # and register our own STMOPresto query runner class
    # which automatically overwrites the default presto query runner
    register(STMOPresto)
    logger.info('Loaded Redash Extension for the custom Presto query runner')
    return stmo_connect
