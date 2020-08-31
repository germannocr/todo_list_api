from navedexapi.exceptions import MissingRequiredFields, InvalidFieldType, InvalidQueryParam, InvalidIdentifier
from navedexapi.mappers import prepare_company_time_filter


def validate_naver_post_body(request_body: dict):
    required_fields = ['name', 'birthdate', 'admission_date', 'job_role', 'projects']
    request_fields = request_body.keys()

    for current_required_field in required_fields:
        if current_required_field not in request_fields:
            raise MissingRequiredFields()
        if not isinstance(current_required_field, str) and current_required_field != 'projects':
            raise InvalidFieldType()


def validate_project_post_body(request_body: dict):
    required_fields = ['name', 'navers']
    request_fields = request_body.keys()

    for current_required_field in required_fields:
        if current_required_field not in request_fields:
            raise MissingRequiredFields()

        if not isinstance(current_required_field, str) and current_required_field == 'name':
            raise InvalidFieldType()

        if not isinstance(current_required_field, list) and current_required_field == 'navers':
            raise InvalidFieldType()


def validate_naver_query_params(query_params: dict):
    possible_query_params = ['name', 'company_time', 'job_role']

    request_query_params_keys = query_params.keys()

    for current_query_param in request_query_params_keys:
        if current_query_param not in possible_query_params:
            raise InvalidQueryParam(code=400)

    if 'company_time' in request_query_params_keys:
        query_params_filters = prepare_company_time_filter(query_params=query_params)

        return query_params_filters
    else:
        return query_params

def validate_project_query_params(query_params: dict):
    possible_query_params = ['name']

    request_query_params_keys = query_params.keys()

    for current_query_param in request_query_params_keys:
        if current_query_param not in possible_query_params:
            raise InvalidQueryParam(code=400)


def validate_object_id(object_id: int):
    if object_id <= 0:
        raise InvalidIdentifier(code=400)
