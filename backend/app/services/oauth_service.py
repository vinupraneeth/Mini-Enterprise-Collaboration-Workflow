from datetime import datetime, timedelta, timezone

import json

import secrets

from urllib.parse import urlencode

from urllib.request import Request as UrlRequest

from urllib.request import urlopen

from fastapi import HTTPException, status

from starlette.responses import RedirectResponse

from sqlalchemy.orm import Session

from app.core.config import (
    FRONTEND_URL,
    GOOGLE_OAUTH_CLIENT_ID,
    GOOGLE_OAUTH_CLIENT_SECRET,
    REFRESH_TOKEN_EXPIRE_DAYS
)

from app.core.security import (
    create_access_token,
    create_refresh_token,
    create_oauth_state_token,
    hash_token,
    verify_oauth_state_token
)

from app.models.auth_token_model import (
    RefreshToken
)

from app.repositories.user_repository import (
    get_user_by_email,
    create_user
)

from app.utils.hashing import (
    hash_password
)

from app.services.saas_service import (
    get_default_organization
)


GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"

GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"

GOOGLE_TOKEN_INFO_URL = "https://oauth2.googleapis.com/tokeninfo"


def is_google_oauth_configured():

    return bool(
        GOOGLE_OAUTH_CLIENT_ID
        and
        GOOGLE_OAUTH_CLIENT_SECRET
    )


def get_google_oauth_status():

    return {

        "configured": is_google_oauth_configured()
    }


def google_login_redirect(
    request
):

    if not is_google_oauth_configured():

        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Google OAuth is not configured"
        )

    redirect_uri = str(
        request.url_for(
            "google_oauth_callback"
        )
    )

    state = create_oauth_state_token(
        {
            "redirect_uri": redirect_uri
        }
    )

    params = {
        "client_id": GOOGLE_OAUTH_CLIENT_ID,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "select_account",
        "state": state
    }

    return RedirectResponse(
        f"{GOOGLE_AUTH_URL}?{urlencode(params)}"
    )


def exchange_google_code(
    code: str,
    redirect_uri: str
):

    body = urlencode(
        {
            "code": code,
            "client_id": GOOGLE_OAUTH_CLIENT_ID,
            "client_secret": GOOGLE_OAUTH_CLIENT_SECRET,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code"
        }
    ).encode("utf-8")

    request = UrlRequest(
        GOOGLE_TOKEN_URL,
        data=body,
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        },
        method="POST"
    )

    with urlopen(request, timeout=10) as response:

        return json.loads(
            response.read().decode("utf-8")
        )


def verify_google_id_token(
    id_token: str
):

    params = urlencode(
        {
            "id_token": id_token
        }
    )

    with urlopen(
        f"{GOOGLE_TOKEN_INFO_URL}?{params}",
        timeout=10
    ) as response:

        user_info = json.loads(
            response.read().decode("utf-8")
        )

    if user_info.get("aud") != GOOGLE_OAUTH_CLIENT_ID:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Google OAuth audience"
        )

    if not user_info.get("email"):

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Google account did not return an email"
        )

    return user_info


def issue_oauth_tokens(
    db: Session,
    user
):

    access_token = create_access_token(
        data={
            "sub": user.email,
            "role": user.role
        }
    )

    refresh_token = create_refresh_token(
        data={
            "sub": user.email
        }
    )

    refresh_token_record = RefreshToken(
        user_id=user.id,
        token_hash=hash_token(refresh_token),
        expires_at=datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
        revoked=False
    )

    db.add(refresh_token_record)

    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


def google_callback(
    request,
    db: Session,
    code: str,
    state: str
):

    state_payload = verify_oauth_state_token(
        state
    )

    redirect_uri = state_payload.get(
        "redirect_uri"
    )

    try:

        token_data = exchange_google_code(
            code,
            redirect_uri
        )

        google_user = verify_google_id_token(
            token_data.get("id_token")
        )

    except HTTPException:

        raise

    except Exception:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Google OAuth verification failed"
        )

    user = get_user_by_email(
        db,
        google_user.get("email")
    )

    if not user:

        organization = get_default_organization(
            db
        )

        user = create_user(
            db,
            {
                "name": google_user.get("name") or google_user.get("email").split("@")[0],
                "email": google_user.get("email"),
                "hashed_password": hash_password(
                    secrets.token_urlsafe(32)
                ),
                "role": "employee",
                "is_active": True,
                "organization_id": organization.id
            }
        )

    if not user.is_active:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )

    token_response = issue_oauth_tokens(
        db,
        user
    )

    params = urlencode(
        {
            **token_response
        }
    )

    return RedirectResponse(
        f"{FRONTEND_URL.rstrip('/')}/oauth/callback?{params}"
    )
