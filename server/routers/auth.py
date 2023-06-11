import os
from sqlmodel import Session
from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from starlette.requests import Request
from utils.config import get_config
from requests_oauthlib import OAuth2Session
from utils.db import get_session
from utils.jwt import create_access_token, get_current_user
from models import User


config = get_config()
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = config.OAUTHLIB_INSECURE_TRANSPORT
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'
router = APIRouter(
    prefix="/auth",
)

github = OAuth2Session(
    client_id=config.GITHUB_ID,
    scope=config.GITHUB_SCOPE
)


@router.get("/github/login/{ref}")
async def github_login(ref: str):
    """Github Login this method for login using github
    flow -> user access /github/login user will be redirect to github login
    and after success login will be direct on github callback
    ref -> this param for redirect to cli or dashboard client
    """
    authorization_base_url = 'https://github.com/login/oauth/authorize'
    direct_github_url, _ = github.authorization_url(
        authorization_base_url, state=ref)
    direct_github_url = direct_github_url
    return RedirectResponse(direct_github_url)


@router.get("/github/callback")
async def github_callback(request: Request, session: Session = Depends(get_session)):
    """Github Callback this method for callback from github
    flow -> after success login on github user will be redirect to this endpoint
    and this endpoint will be call github api to get user data
    aftter get user data wi will be create user on database and create jwt token
    and redirect to cli or dashboard client
    """
    ref = request.query_params.get('state')
    token_url = 'https://github.com/login/oauth/access_token'
    redirect_response = request.url.__str__()
    github.fetch_token(token_url, client_secret=config.GITHUB_SECRET,
                       authorization_response=redirect_response)
    github_user = github.get("https://api.github.com/user").json()
    redirect_url = config.CLI_REDIRECT_URL if ref == "cli" else config.DASHBOARD_REDIRECT_URL
    user = session.query(User).filter(
        User.github_id == str(github_user['id'])).first()
    if user is None:
        user = User(name=github_user['name'], email=github_user['email'], github_id=str(
            github_user['id']))
        session.add(user)
        session.commit()
    token = create_access_token(user.id)
    return RedirectResponse(f"{redirect_url}?token={token}")


@router.get("/me")
async def me(user: User = Depends(get_current_user)):
    """Me this method for get user data
    flow -> user access /auth/me and will be get user data from jwt token
    """
    return user
