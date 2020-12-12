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
$ curl -X POST "http://localhost:5000/api/v1/cert/" -H  "accept: application/json" -H  "Content-Type: multipart/form-data" -F "file=@certificate.pem;type=application/x-x509-ca-cert"
```
Example response:
```
{
    "version": 3,
    "serialNumber": "18:ac:b5:6a:fd:69:b6:15:3a:63:6c:af:da:fa:c4:a1",
    "subject": "C=US,O=GeoTrust Inc.,CN=GeoTrust Primary Certification Authority",
    "issuer": "C=US,O=GeoTrust Inc.,CN=GeoTrust Primary Certification Authority",
    "notBefore": "2006-11-27T00:00:00Z",
    "notAfter": "2036-07-16T23:59:59Z",
    "expired": false,
    "signatureAlgorithm": "sha1WithRSAEncryption",
    "extensions": {
        "subjectKeyIdentifier": {
            "critical": false,
            "data": [
                "2C:D5:50:41:97:15:8B:F0:8F:36:61:5B:4A:FB:6B:D9:99:C9:33:92"
            ]
        },
        "keyUsage": {
            "critical": true,
            "data": [
                "Certificate Sign",
                "CRL Sign"
            ]
        },
        "basicConstraints": {
            "critical": true,
            "data": [
                "CA:TRUE"
            ]
        }
    }
}
```