
import strawberry as sb
import uvicorn
from fastapi import FastAPI

from deriving_excellent_mortgage_insights import mutations, queries
from strawberry.asgi import GraphQL

schema = sb.Schema(
    query=queries.Query,
    mutation=mutations.Mutation
)

graphql_app = GraphQL(schema=schema)

app = FastAPI()
app.add_route("/graphql", graphql_app)
app.add_websocket_route("/graphql", graphql_app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
