import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from core.config import app_settings
from api import api, files

app = FastAPI(
    title='FILE STORAGE',
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


app.include_router(api.api_router, prefix='')
app.include_router(files.files_router, prefix='/files')

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=app_settings.project_host,
        port=app_settings.project_port,
        reload=True,
        log_level='info'
    )
