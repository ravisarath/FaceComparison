from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader
from starlette import status
import os


X_API_KEY = APIKeyHeader(name='key')


def get_apiauth_object_by_key():
    """
    authentication for an API key.
    @param inp: none
    @return: key.
    """
    return os.getenv("API_AUTH_KEY")


def check_authentication_header(x_api_key: str = Depends(X_API_KEY)):
    """ takes the X-API-Key header and converts it into the matching user object from the database """

    # this is where the SQL query for converting the API key into a user_id will go
    if x_api_key != get_apiauth_object_by_key():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )
