#!/usr/bin/env python3
"""Finding schools by topic"""


def schools_by_topic(mongo_collection, topic):
    """Finds schools teaching a topic

    Args:
        mongo_collection: The collection object
        topic: The topic being searched for

    Returns:
        List of schools teaching the topic
    """
    result = mongo_collection.find({"topics": topic})
    return list(result)
