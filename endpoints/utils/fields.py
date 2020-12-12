from flask_restx import fields

TIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'


class CustomDateTime(fields.Raw):
    __schema_type__ = 'string'
    __schema_format__ = 'date-time'

    def __init__(self, dt_format=TIME_FORMAT, **kwargs):
        super(CustomDateTime, self).__init__(**kwargs)
        self.dt_format = dt_format

    def format(self, value):
        try:
            return value.strftime(self.dt_format)
        except AttributeError as ae:
            raise fields.MarshallingException(ae)
