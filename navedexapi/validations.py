from navedexapi.exceptions import MissingRequiredFields, InvalidFieldType


def validate_post_body(request_body: dict):
    required_fields = ['name', 'birthdate', 'admission_date', 'job_role', 'projects']
    request_fields = request_body.keys()

    for current_required_field in required_fields:
        if current_required_field not in request_fields:
            raise MissingRequiredFields()
        if not isinstance(current_required_field, str) and current_required_field != 'projects':
            raise InvalidFieldType()


def validate_naver_query_params(query_params: dict):
    possible_query_params = ['name', 'company-time', 'job-role']

    request_query_params_keys = query_params.keys()

    for current_query_param in request_query_params_keys:
        if current_query_param not in possible_query_params:
            #TODO Exceção para query param incorreto
            raise Exception


def validate_project_query_params(query_params: dict):
    possible_query_params = ['name']

    request_query_params_keys = query_params.keys()

    for current_query_param in request_query_params_keys:
        if current_query_param not in possible_query_params:
            #TODO Exceção para query param incorreto
            raise Exception


def validate_object_id(object_id: int):
    if object_id <= 0:
        #TODO Fazer exceção para ID invalido
        raise Exception