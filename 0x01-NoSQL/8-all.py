#!/usr/bin/env python3
"""Listing all the documents in a collection"""


def list_all(mongo_collection):
    """Returns list of all documents in a collection

    Args:
        mongo_collection: The collection object

    Returns:
        The list of all documents in the collection.
        An empty list if there are no documents in the collection
    """
    result = mongo_collection.find({})
    return list(result)
