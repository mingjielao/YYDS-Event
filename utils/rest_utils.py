import copy
from flask import request
import json
import logging
from datetime import datetime

logger = logging.getLogger()


class RESTContext:
    _default_limit = 10

    def __init__(self, request_context, path_parameters=None):
        log_message = ""
        self.limit = RESTContext._default_limit
        self.path = request_context.path
        self.args = dict(request_context.args)

        self.offset = self.args.get("offset")
        if "limit" in self.args:
            self.limit = self.args.get("limit")

        self.filtered_args()

        self.path = request.path
        self.data = None
        self.headers = dict(request.headers)
        self.method = request.method
        self.host_url = request.host_url
        self.full_path = request.full_path
        self.base_url = request.base_url

        self.fields = None

    def filtered_args(self):
        if "offset" in self.args:
            self.args.pop("offset")
        if "limit" in self.args:
            self.args.pop("limit")