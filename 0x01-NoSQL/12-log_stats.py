#!/usr/bin/env python3
"""Stats finder for logs"""
from pymongo import MongoClient


def print_nginx_request_logs(nginx_collection):
    """Prints stats about Nginx request logs."""
    total_logs = nginx_collection.count_documents({})
    print(f"{total_logs} logs")
 
    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        method_count = nginx_collection.count_documents({"method": method})
        print(f"\tmethod {method}: {method_count}")
 
    status_checks = nginx_collection.count_documents({"method": "GET",
                                                      "path": "/status"})
    print(f"{status_checks} status check")


def run():
    """Provides some stats about Nginx logs stored in MongoDB."""
    client = MongoClient('mongodb://127.0.0.1:27017')
    print_nginx_request_logs(client.logs.nginx)
    client.close()


if __name__ == '__main__':
    run()
