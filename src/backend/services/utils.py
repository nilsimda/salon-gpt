import io

from fastapi import Request
from pypdf import PdfReader


def get_header_value(headers: list, keys: list) -> str:
    for k, v in headers:
        if k.decode("utf-8") in keys:
            return v.decode("utf-8")
    return ""
