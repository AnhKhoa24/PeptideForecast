from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from app.core.oauth_google import get_google_authorize_url, get_google_user_info
from app.model.user import get_or_create_user
from app.core.security import create_jwt_token
# from bson import ObjectId 
from fastapi.responses import HTMLResponse
import json

router = APIRouter()

@router.get("/login/google")
async def login_google():
    url = await get_google_authorize_url()
    return RedirectResponse(url)

@router.get("/callback")
async def google_callback(code: str):
    user_info = await get_google_user_info(code)
    user = await get_or_create_user(user_info)
    user["_id"] = str(user["_id"])
    token = create_jwt_token(user["email"])

    # 👉 CHUYỂN dict Python → JSON string
    user_json = json.dumps(user)

    html_content = f"""
    <html><body>
      <script>
        window.opener.postMessage({{
          access_token: "{token}",
          user: {user_json}
        }}, "*");
        window.close();
      </script>
      <p>Đang đăng nhập...</p>
    </body></html>
    """

    return HTMLResponse(content=html_content)