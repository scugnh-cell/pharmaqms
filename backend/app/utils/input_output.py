import inspect
from functools import wraps
from flask import Response, jsonify
from app.utils import logger

RET_CODE_SUCCESS = 200
RET_CODE_ERROR = 500
LONG_ERROR_MSG_LENGTH = 200


def cut_long_error_msg(data):
    if isinstance(data, str):
        if len(data) > LONG_ERROR_MSG_LENGTH:
            return "%s ..." % data[0:LONG_ERROR_MSG_LENGTH]
    elif isinstance(data, list):
        for i, sub_d in enumerate(data):
            data[i] = cut_long_error_msg(sub_d)
    elif isinstance(data, dict):
        for k, sub_d in data.items():
            data[k] = cut_long_error_msg(sub_d)
    return data


def format_output(success, msg):
    if not success:
        logger.error(msg)
        msg = cut_long_error_msg(msg)
    response = {
        "data": msg,
        "success": 1 if success else 0,
    }
    return jsonify(response)


def json_output(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        ret = func(*args, **kwargs)
        if isinstance(ret, Response):
            return ret
        succ, msg = ret
        if isinstance(msg, Response):
            return msg
        return format_output(succ, msg)

    wrapper.__signature__ = inspect.signature(func)
    return wrapper
