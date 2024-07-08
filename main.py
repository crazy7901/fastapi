from path import Path
from common import log
import uvicorn
from core.registrar import register_app
app = register_app()

if __name__ == '__main__':
    try:
        uvicorn.run(
            app=f'{Path(__file__).stem}:app',
            host='0.0.0.0',
            port=8080,
            reload=True,
        )
    except Exception as e:
        # log.error(f'❌ FastAPI start filed: {e}')
        print(e)