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


class InvalidFieldValue(APIException):
    status_code = 400
    default_detail = "Invalid or incorrect value of one of the fields in the request."
    default_code = "incorrect_field_value"


class EmprestimoAlreadyPaid(APIException):
    status_code = 400
    default_detail = "The loan related to this payment has already had its debit balance paid in full."
    default_code = "emprestimo_already_paid"