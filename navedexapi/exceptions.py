from rest_framework.exceptions import APIException


class MissingRequiredFields(APIException):
    status_code = 400
    default_detail = "Missing required field. " \
                     "Please send all the necessary fields, including title, description and url of the image."
    default_code = "missing_required_field"


class InvalidFieldType(APIException):
    status_code = 400
    default_detail = "Invalid or incorrect type of one of the fields in the request."
    default_code = "incorrect_field_type"


class InvalidQueryParam(APIException):
    status_code = 400
    default_detail = "Invalid or incorrect query param in the request."
    default_code = "incorrect_query_param"


class InvalidIdentifier(APIException):
    status_code = 400
    default_detail = "Invalid or incorrect object unique identifier in the request."
    default_code = "incorrect_identifier"


class NaverNotFound(APIException):
    status_code = 404
    default_detail = "Naver object not found."
    default_code = "naver_not_found"


class ProjectNotFound(APIException):
    status_code = 404
    default_detail = "Project object not found."
    default_code = "project_not_found"
