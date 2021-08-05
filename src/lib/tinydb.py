from tinydb import TinyDB
from tinydb.middlewares import CachingMiddleware
from tinydb.storages import JSONStorage

db = TinyDB("dps.json", storage=CachingMiddleware(JSONStorage))
