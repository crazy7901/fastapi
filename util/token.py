import datetime
from fastapi import HTTPException
import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from app.crud.crud_user import user_dao
from db.database import async_db_session

SECURITY_KEY = 'cdsbfjknjkvnuidlnfuidhfusdlbdvnu'
ALGORITHMS = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")


async def generate_access_token(username: str):
    if not username:
        raise HTTPException(
            status_code=401,
            detail="incorrect username and password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    # 如果存在生成token
    token_expires = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=100)
    print("token_expires:", token_expires)
    # 需要加密的数据
    token_data = {
        'username': username,
        'exp': token_expires
    }
    token = jwt.encode(token_data, SECURITY_KEY, ALGORITHMS)

    return token


# token解析验证
async def get_current_token(token: str = Depends(oauth2_scheme)):
    print("获取token:", token)
    uauth_exp = HTTPException(status_code=401, detail=' do you provide token none...:UnAuthorized')
    data_info = {
        "username": "",
        "exist": False
    }
    exist_user = None
    try:
        # 解码
        token_data = jwt.decode(token, SECURITY_KEY, ALGORITHMS)
        if token_data:
            # 验证
            username = token_data.get('username', None)
            async with async_db_session.begin() as db:
                user = await user_dao.get(db=db, name=username)
            if user:
                isValidate = True
            else:
                isValidate = False
            if isValidate:
                data_info['exist'] = isValidate
                data_info['username'] = username
            else:
                data_info['exist'] = None
    except Exception as error:
        raise uauth_exp
    if not data_info:
        raise uauth_exp
    return data_info
