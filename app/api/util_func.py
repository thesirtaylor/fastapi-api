import json
import pickle
from fastapi import HTTPException

def http_exception(status_code, detail, header=None):
    return HTTPException(status_code, detail, header)

def success_response(data):
    return { "data": data}