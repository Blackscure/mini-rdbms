def validate_user(data):
    if "id" not in data or "name" not in data:
        raise ValueError("Invalid user payload")