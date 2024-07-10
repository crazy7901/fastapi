import uvicorn
from fastapi import FastAPI
from app.router import router
app = FastAPI()
app.include_router(router)
if __name__ == '__main__':
    try:
        uvicorn.run(
            app='main:app',
            host='0.0.0.0',
            port=8080,
            reload=True,
        )
    except Exception as e:
        # log.error(f'❌ FastAPI start filed: {e}')
        print(e)