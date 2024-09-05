import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.router import router
app = FastAPI()
# 配置 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有HTTP方法
    allow_headers=["*"],  # 允许所有HTTP头
)

app.include_router(router)
if __name__ == '__main__':
    try:
        uvicorn.run(
            app='main:app',
            host='0.0.0.0',
            port=8000,
            reload=True,
        )
    except Exception as e:
        # log.error(f'❌ FastAPI start filed: {e}')
        print(e)