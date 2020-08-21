from conaferapi.models import User, Post


def create_post(request_body: dict, user: User):
    created_model = Post.objects.create(
        title=request_body.get("title"),
        description=request_body.get("description"),
        image_src=request_body.get("image-url"),
        created_by_user=user.id
    )

    return created_model
