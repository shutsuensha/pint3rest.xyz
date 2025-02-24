import strawberry
from strawberry.fastapi import GraphQLRouter
from .queries import Query
from .mutations import Mutation
from app.api.graphql.context import get_context
from fastapi import APIRouter

schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema, context_getter=get_context)


"""
query {
  getUsers {
    id
    username
  }
}


query {
  getUserById(userId: 1) {
    id
    username
  }
}


mutation {
  createUser(username: "new_username") {
    id
    username
  }
}

mutation {
  updateUserUsername(userId: 1, newUsername: "updated_username") {
    id
    username
  }
}

mutation {
  deleteUser(userId: 1)
}
"""