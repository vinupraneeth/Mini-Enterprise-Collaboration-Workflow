from fastapi import (
    APIRouter,
    Depends,
    Request
)

from fastapi.security import (
    OAuth2PasswordRequestForm
)

from sqlalchemy.orm import Session

from app.db.deps import get_db

from app.schemas.user_schema import (
    UserCreate,
    UserResponse,
    LoginRequest,
    TokenResponse,
    RefreshTokenRequest,
    PasswordResetRequest,
    PasswordResetRequestResponse,
    PasswordResetConfirm,
    PasswordResetConfirmResponse
)

from app.services.user_service import (
    register_user,
    login_user,
    refresh_access_token,
    request_password_reset,
    confirm_password_reset
)

from app.services.oauth_service import (
    get_google_oauth_status,
    google_login_redirect,
    google_callback
)

from app.core.dependencies import (
    get_current_user,
    require_admin
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201
)
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    return register_user(
        db,
        user
    )


@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    login_data = LoginRequest(
        email=form_data.username,
        password=form_data.password
    )

    return login_user(
        db,
        login_data
    )


@router.post(
    "/refresh",
    response_model=TokenResponse
)
def refresh_token(
    token_data: RefreshTokenRequest,
    db: Session = Depends(get_db)
):

    return refresh_access_token(
        db,
        token_data
    )


@router.post(
    "/password-reset/request",
    response_model=PasswordResetRequestResponse
)
def password_reset_request(
    reset_data: PasswordResetRequest,
    db: Session = Depends(get_db)
):

    return request_password_reset(
        db,
        reset_data
    )


@router.post(
    "/password-reset/confirm",
    response_model=PasswordResetConfirmResponse
)
def password_reset_confirm(
    reset_data: PasswordResetConfirm,
    db: Session = Depends(get_db)
):

    return confirm_password_reset(
        db,
        reset_data
    )


@router.get(
    "/google/status"
)
def google_status():

    return get_google_oauth_status()


@router.get(
    "/google"
)
def google_login(
    request: Request
):

    return google_login_redirect(
        request
    )


@router.get(
    "/google/callback",
    name="google_oauth_callback"
)
def google_oauth_callback(
    request: Request,
    code: str,
    state: str,
    db: Session = Depends(get_db)
):

    return google_callback(
        request,
        db,
        code,
        state
    )


@router.get(
    "/me",
    response_model=UserResponse
)
def get_me(
    current_user = Depends(get_current_user)
):

    return current_user


@router.get(
    "/admin-only"
)
def admin_only_route(
    current_user = Depends(require_admin)
):

    return {
        "message": f"Welcome Admin {current_user.name}"
    }
