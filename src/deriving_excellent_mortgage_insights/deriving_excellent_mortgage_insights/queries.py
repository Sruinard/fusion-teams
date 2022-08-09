import strawberry as sb


@sb.type
class Query:
    @sb.field
    def get_info(self) -> str:
        return "Hello World"
