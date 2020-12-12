from flask import request, abort
from flask_restx import Namespace, Resource, fields
import OpenSSL
from datetime import datetime
from werkzeug.datastructures import FileStorage
from .utils.fields import CustomDateTime

ASM1_TIME_FORMAT = '%Y%m%d%H%M%SZ'
ENCODING = 'utf-8'

api = Namespace('cert', description='x509 certificate validation')

extension_model = api.model(
    'Extension',
    dict(
        critical=fields.Boolean,
        data=fields.List(fields.String)
    )
)

extension_fields = {'*': fields.Wildcard(fields.Nested(extension_model))}

certificate_model = api.model(
    'Certificate',
    dict(
        version=fields.Integer,
        serialNumber=fields.String,
        subject=fields.String,
        issuer=fields.String,
        notBefore=CustomDateTime(example='2020-01-01T00:00:00Z'),
        notAfter=CustomDateTime(example='2020-12-31T23:59:59Z'),
        expired=fields.Boolean,
        signatureAlgorithm=fields.String,
        extensions=fields.Nested(
            api.model(
                "extensions", {
                    "*": fields.Wildcard(
                        fields.Nested(extension_model)
                    )
                }
            )
        )
    )
)

upload_parser = api.parser()
upload_parser.add_argument('file', location='files',
                           type=FileStorage, required=True)


@api.route('/')
class CertificateEndpoint(Resource):
    @api.expect(upload_parser)
    @api.marshal_with(certificate_model)
    @api.response(400, 'Bad Request')
    def post(self):
        args = upload_parser.parse_args()

        if 'file' not in args:
            return abort(400)

        file = args['file']

        if file:
            content = file.read()
            crt = OpenSSL.crypto.load_certificate(
                OpenSSL.crypto.FILETYPE_PEM, content)
            crt_out = create_certificate(crt)
            return crt_out

        return abort(400)


def parse_asn1_time(t):
    return datetime.strptime(t.decode(ENCODING), ASM1_TIME_FORMAT)


def x509name_to_str(name):
    attrs = [x[0].decode(ENCODING) + '=' + x[1].decode(ENCODING)
             for x in name.get_components()]
    return ",".join(attrs)


def serial_number_to_str(s):
    serial_hex = hex(s)
    serial_parts = [serial_hex[x:x+2] for x in range(0, len(serial_hex), 2)]
    return ':'.join(serial_parts[1:])


def create_certificate(crt):
    return {
        'version': crt.get_version()+1,
        'serialNumber': serial_number_to_str(crt.get_serial_number()),
        'subject': x509name_to_str(crt.get_subject()),
        'issuer': x509name_to_str(crt.get_issuer()),
        'notBefore': parse_asn1_time(crt.get_notBefore()),
        'notAfter': parse_asn1_time(crt.get_notAfter()),
        'expired': crt.has_expired(),
        'signatureAlgorithm': crt.get_signature_algorithm().decode(ENCODING),
        'extensions': create_extensions(crt)
    }


def create_extensions(crt):
    extensions = dict()
    for x in range(crt.get_extension_count()):
        ext = crt.get_extension(x)
        extensions[ext.get_short_name().decode(
            ENCODING)] = create_extension(ext)
    return extensions


def create_extension(ext):
    return {
        'critical': bool(ext.get_critical()),
        'data': str(ext).split(', ')
    }
