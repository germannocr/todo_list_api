import json
from django.http import JsonResponse
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from emprestimo_api.exceptions import EmprestimoNotFound
from rest_framework.decorators import (
    api_view,
    permission_classes
)
from emprestimo_api.serializers import (
    EmprestimoSerializer,
    PagamentoSerializer
)
from emprestimo_api.validations import (
    validate_emprestimo_post_body,
    validate_pagamento_post_body,
    validate_saldo_devedor
)
from emprestimo_api.persistency import (
    create_emprestimo,
    retrieve_all_emprestimos,
    retrieve_all_pagamentos,
    create_pagamento,
    retrieve_emprestimo
)
from emprestimo_api.mappers import (
    create_custom_fields,
    map_post_emprestimo_response,
    map_get_emprestimo_response,
    map_get_pagamento_response,
    map_post_pagamento_response,
    update_debit_balance
)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_emprestimo(request):
    """
    Creates a new Emprestimo, performing all necessary validations.

    #Parameters:
        request (WSGIRequest): WSGIRequest type object which represents the request made by the user,
                               passing necessary information to create the object and about the user
                               who made the request.

    #Returns:
        mapped_response (JSON Response): Response, in JSON format, with the information of the created object.
    """
    request_body = json.loads(request.body)
    user = request.user
    try:
        request_body = create_custom_fields(request_body)
        validate_emprestimo_post_body(request_body=request_body)
        new_emprestimo = create_emprestimo(request_body=request_body,
                                           request_user=user)
        serializer_response = EmprestimoSerializer(new_emprestimo)
        mapped_response = map_post_emprestimo_response(serializer_response)
        return mapped_response

    except APIException as custom_exception:
        return JsonResponse({
            'more info': custom_exception.default_detail
        },
            safe=False,
            status=custom_exception.status_code
        )

    except Exception as exception:
        return JsonResponse({
            'error': str(exception)
        },
            safe=False,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def retrieve_emprestimo_list(request):
    """
    Retrieve a list of Emprestimo objects, performing all necessary validations.

    #Parameters:
        request (WSGIRequest): WSGIRequest type object which represents the request made by the user,
                               passing necessary information to retrieve the objects list and about the user
                               who made the request.

    #Returns:
        mapped_response (JSON Response): Response, in JSON format, with the information of the objects found.
    """
    user = request.user
    try:
        retrieved_emprestimo_list = retrieve_all_emprestimos(user_id=user.id)
        serialized_response = EmprestimoSerializer(retrieved_emprestimo_list, many=True)
        return map_get_emprestimo_response(serialized_response)

    except APIException as custom_exception:
        return JsonResponse({
            'more info': custom_exception.default_detail
        },
            safe=False,
            status=custom_exception.status_code
        )

    except Exception as exception:
        return JsonResponse({
            'error': str(exception)
        },
            safe=False,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def retrieve_pagamento_list(request):
    """
    Retrieve a list of Pagamento objects, performing all necessary validations.

    #Parameters:
        request (WSGIRequest): WSGIRequest type object which represents the request made by the user,
                               passing necessary information to retrieve the objects list and about the user
                               who made the request.

    #Returns:
        mapped_response (JSON Response): Response, in JSON format, with the information of the objects found.
    """
    user = request.user
    try:
        retrieved_pagamentos_list = retrieve_all_pagamentos(user_id=user.id)

        serialized_response = PagamentoSerializer(retrieved_pagamentos_list, many=True)
        return map_get_pagamento_response(serialized_response)

    except APIException as custom_exception:
        return JsonResponse({
            'more info': custom_exception.default_detail
        },
            safe=False,
            status=custom_exception.status_code
        )

    except Exception as exception:
        return JsonResponse({
            'error': str(exception)
        },
            safe=False,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_pagamento(request):
    """
    Creates a new Pagamento, performing all necessary validations.

    #Parameters:
        request (WSGIRequest): WSGIRequest type object which represents the request made by the user,
                               passing necessary information to create the object and about the user
                               who made the request.

    #Returns:
        mapped_response (JSON Response): Response, in JSON format, with the information of the created object.
    """
    request_body = json.loads(request.body)
    user = request.user
    emprestimo_identifier = request_body.get('identificador_emprestimo')
    try:
        validate_pagamento_post_body(request_body=request_body)
        retrieved_emprestimo = retrieve_emprestimo(emprestimo_id=emprestimo_identifier, user_id=user.id)
        if retrieved_emprestimo:
            validate_saldo_devedor(retrieved_emprestimo=retrieved_emprestimo)
            update_debit_balance(request_body=request_body, retrieved_emprestimo=retrieved_emprestimo)
            new_pagamento = create_pagamento(request_body=request_body,
                                             request_user=user)
            serializer_response = PagamentoSerializer(new_pagamento)
            mapped_response = map_post_pagamento_response(serializer_response)
            return mapped_response
        else:
            raise EmprestimoNotFound(code=404)

    except APIException as custom_exception:
        return JsonResponse({
            'more info': custom_exception.default_detail
        },
            safe=False,
            status=custom_exception.status_code
        )

    except Exception as exception:
        return JsonResponse({
            'error': str(exception)
        },
            safe=False,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
