from rest_framework.exceptions import APIException


class MissingRequiredFields(APIException):
    status_code = 400
    default_detail = "Missing required field. " \
                     "Please send all the necessary fields, including title, description and url of the image."
    default_code = "missing_required_field"


class InvalidFieldType(APIException):
    status_code = 400
    default_detail = "Invalid or incorrect type of one of the fields in the request. All fields are of type string."
    default_code = "incorrect_field_type"
