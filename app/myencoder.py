import json

from app.api.validationresponse import ValidationResponse

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ValidationResponse):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)