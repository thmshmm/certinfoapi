# CertInfo API

REST API to validate x509 certificates.

# API documentation (Swagger)

URL: \<HOST\>/api/v1/

## Testing

Run the service:
```
$ python3 app.py
```

Query the **cert** endpoint:
```
$ curl -X "POST" "http://localhost:5000/api/v1/cert" \
       -H 'Content-Type: multipart/form-data; charset=utf-8;' \
       -F "file=@certificate.pem"
```
