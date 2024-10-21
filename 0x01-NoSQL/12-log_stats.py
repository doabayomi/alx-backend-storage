#!/usr/bin/env python3
from pymongo import MongoClient

"""Finding total logs"""
client = MongoClient('mongodb://localhost:27017')
nginx_logs = client.logs.nginx
total_logs = nginx_logs.count_documents({})
print(f"{total_logs} logs")

"""Finding count for each method"""
print("Methods:")
methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
for method in methods:
    method_count = nginx_logs.count_documents({"\tmethod": method})
    print(f"method {method}: {method_count}")

"""Finding total status checks"""
status_checks = nginx_logs.count_documents({"method": "GET",
                                            "path": "/status"})
print(f"{status_checks} status check")
