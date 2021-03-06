from datetime import datetime
from django.contrib.auth.models import User
from todo_list_api.models import (
    Card
)


def delete_retrieved_card(retrieved_card: Card):
    retrieved_card.delete()

    return


def update_retrieved_card(retrieved_card: Card, request_body: dict):
    if request_body.get('name'):
        retrieved_card.name = request_body.get('name')
    if request_body.get('description'):
        retrieved_card.description = request_body.get('description')
    if request_body.get('status'):
        retrieved_card.status = request_body.get('status')

    retrieved_card.save()

    return


def retrieve_todo_cards_list(user_id: int):
    retrieved_card = Card.objects.filter(status='todo', created_by_user=user_id).all()

    return retrieved_card


def retrieve_doing_cards_list(user_id: int):
    retrieved_card = Card.objects.filter(status='doing', created_by_user=user_id).all()

    return retrieved_card


def retrieve_done_cards_list(user_id: int):
    retrieved_card = Card.objects.filter(status='done', created_by_user=user_id).all()

    return retrieved_card


def retrieve_card_by_id(card_id: int, user_id: int):
    retrieved_card = Card.objects.filter(id=card_id, created_by_user=user_id).first()

    return retrieved_card


def create_card(request_body: dict, request_user: User):
    """
    Creates a new object of type Card.

    #Parameters:
        request_body (dict):Body in JSON format with the necessary fields for creating a new Card.
        request_user (User):User type object that represents the user who made the request.

    #Returns:
        created_card (Card):New object of type Card created.
    """
    created_card = Card.objects.create(
        name=request_body.get('name'),
        description=request_body.get('description'),
        status=request_body.get('status'),
        created_by_user=request_user.id
    )

    return created_card
