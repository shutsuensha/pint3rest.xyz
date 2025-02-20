import strawberry


@strawberry.type
class User:
    id: int
    username: str
