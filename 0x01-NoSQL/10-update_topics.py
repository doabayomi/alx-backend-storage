#!/usr/bin/env python3
"""Updating school topics by name"""


def update_topics(mongo_collection, name, topics):
    """Updates the topics of a school based on name

    Args:
        mongo_collection: The collection (school) object
        name: The name of the school to update
        topics: The list of topics to update
    """
    mongo_collection.update_many(
        {"name": name},
        {"$set": {"topics": topics}}
    )
