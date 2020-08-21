from conaferapi.exceptions import MissingRequiredFields, InvalidFieldType


def validate_post_body(request_body: dict):
    required_fields = ['title', 'description', 'image-url']
    request_fields = request_body.keys()

    for current_required_field in required_fields:
        if current_required_field not in request_fields:
            raise MissingRequiredFields()
        if not isinstance(current_required_field, str):
            raise InvalidFieldType()

