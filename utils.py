# NOTE: you should use pymongo.MongoClient(...) rather than from pymongo import MongoClient
import pymongo
import mongomock


def get_db_handle(host, port, username, password):
    client = pymongo.MongoClient(
        host=host, port=int(port), username=username, password=password
    )
    return client


def get_db_handle_mock():
    return mongomock.MongoClient()
