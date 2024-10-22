#!/usr/bin/env python3
"""Stats finder for logs"""
from pymongo import MongoClient

if __name__ == '__main__':
    """Finding total logs"""
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_logs = client.logs.nginx
    total_logs = nginx_logs.count_documents({})
    print(f"{total_logs} logs")

    """Finding count for each method"""
    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        method_count = nginx_logs.count_documents({"method": method})
        print(f"\tmethod {method}: {method_count}")

    """Finding total status checks"""
    status_checks = nginx_logs.count_documents({"method": "GET",
                                                "path": "/status"})
    print(f"{status_checks} status check")

    client.close()
