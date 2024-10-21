#!/usr/bin/env python3
"""Inserting a new document into collection"""


def insert_school(mongo_collection, **kwargs):
    """Inserts a new document into a collection

    Args:
        mongo_collection: The collection object

    Returns:
        The _id of the new document
    """
    data = kwargs
    result = mongo_collection.insert_one(data)
    return result.inserted_id
