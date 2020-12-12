from flask import Blueprint
from flask_restx import Api
from .cert import api as cert_ns

API_PREFIX = '/api/v1'

blueprint = Blueprint('api', __name__, url_prefix=API_PREFIX)
api = Api(
    blueprint,
    title='CertInfo API',
    version='1.0',
    description='REST API for x509 certificate validation'
)

api.add_namespace(cert_ns)
