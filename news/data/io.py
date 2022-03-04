import json
from typing import Any, Dict, List

from lz4 import frame
from datetime import date, datetime


def json_reader(file_path: str) -> List[Dict[str, Any]]:
    """
    Loads dictionary from json format which also compressed with lz4
    """
    with frame.open(filename=file_path, mode="r") as f:
        decoded_data = f.read().decode()
    jsonfied_data = json.loads(decoded_data)
    return jsonfied_data


def json_writer(file_path: str, data: List[Dict[str, Any]]) -> None:
    """
    Dumps dictionary into json format compressed with lz4
    """
    encoded_data = json.dumps(data, default=json_serial).encode()
    with frame.open(filename=file_path, mode="wb") as f:
        f.write(encoded_data)


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))
