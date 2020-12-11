from flask import Flask, request, abort
import json
import OpenSSL
import secrets
from datetime import datetime


app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(32)
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024

API_PREFIX = '/api/v1'
ASM1_TIME_FORMAT = '%Y%m%d%H%M%SZ'
OUTPUT_TIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
ENCODING = 'utf-8'


@app.route('/')
def hello():
    return 'Hello, World!'


@app.route(API_PREFIX+'/cert', methods=['POST'])
def certificate():
    if 'file' not in request.files:
        return abort(400)

    file = request.files['file']

    if file:
        content = file.read()
        crt = OpenSSL.crypto.load_certificate(
            OpenSSL.crypto.FILETYPE_PEM, content)
        crt_out = create_certificate(crt)
        pretty = 4 if request.args.get('pretty') != None else None
        return json.dumps(crt_out, indent=pretty)

    return abort(400)


def parse_asn1_time(t):
    return datetime.strptime(t.decode(ENCODING), ASM1_TIME_FORMAT)


def format_time(t):
    return t.strftime(OUTPUT_TIME_FORMAT)


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
        'notBefore': format_time(parse_asn1_time(crt.get_notBefore())),
        'notAfter': format_time(parse_asn1_time(crt.get_notAfter())),
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


if __name__ == "__main__":
    app.run(port=5000, debug=True)
