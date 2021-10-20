from flask import Flask, Response, request
from flask_cors import CORS
import json
import logging

from utils import rest_utils
from middleware.service_factory import ServiceFactory
from application_services.event_service import EventResource
from Framework.RDBService import RDBService as RDBService

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():
    return '<u>Hello World!</u>'


@app.route('/api/<resource_collection>', methods=["GET", "POST"])
def do_resource_collection(resource_collection):

    request_inputs = rest_utils.RESTContext(request, resource_collection)
    service = ServiceFactory()
    svc = service.get_service(resource_collection)

    if request_inputs.method == "GET":
        res = svc.get_by_template(request_inputs.args,
                                  field_list=request_inputs.fields,
                                  limit=request_inputs.limit,
                                  offset=request_inputs.offset
                                  )
        # res = request_inputs.add_pagination(res)
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")

    elif request_inputs.method == "POST":
        res = svc.create(request_inputs.args)
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")

    return rsp


@app.route('/api/<resource_collection>/<resource_id>', methods=["GET", "POST", "DELETE"])
def specific_resource(resource_collection, resource_id):
    request_inputs = rest_utils.RESTContext(request, resource_collection)
    service = ServiceFactory()
    svc = service.get_service(resource_collection)

    if request_inputs.method == "GET":
        res = svc.get_by_resource_id(resource_id)
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
    elif request_inputs.method == "DELETE":
        res = svc.delete_by_resource_id(resource_id)
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
    return rsp


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
