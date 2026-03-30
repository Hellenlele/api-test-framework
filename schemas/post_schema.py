CREATE_POST_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "id":     {"type": "integer"},
        "title":  {"type": "string"},
        "body":   {"type": "string"},
        "userId": {"type": "integer"}
    },
    "required": ["id", "title", "body", "userId"]
}
