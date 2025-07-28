from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer  # Change this import
from .auth import decode_token

oauth2_scheme = HTTPBearer()  # Change this from OAuth2PasswordBearer to HTTPBearer

def get_current_user_role(token: str = Depends(oauth2_scheme)):
    # Since HTTPBearer returns an HTTPAuthorizationCredentials object,
    # you need to get the token string from token.credentials
    token_str = token.credentials

    payload = decode_token(token_str)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    role = payload.get("role")

    if role is None:
        raise HTTPException(status_code=401, detail="Role not found in token")
    return role

def role_required(required_role: str):
    def role_checker(role: str = Depends(get_current_user_role)):
        if role != required_role:
            raise HTTPException(status_code=403, detail="Operation not permitted for this role")
        return role
    return role_checker
