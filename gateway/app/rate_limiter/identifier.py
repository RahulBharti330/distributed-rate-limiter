from fastapi import Request


async def identify_request(request: Request) -> str:
    """
    Identify the client making the request.
    Priority:
    1. API Key
    2. Authenticated User ID
    3. IP Address
    """

    api_key = request.headers.get("X-API-Key")
    if api_key:
        return f"apikey:{api_key}"

    user_id = request.headers.get("X-User-Id")
    if user_id:
        return f"user:{user_id}"

    client_ip = request.client.host if request.client else "unknown"
    return f"ip:{client_ip}"
