# --------------------------------------------------------------------------
# FastAPI application과 runner을 선언하는 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from __future__ import annotations

import uvicorn

from src import create_app, init_logger
from src.core.settings import AppSettings

app_settings = AppSettings()
init_logger(app_settings)


app = create_app(app_settings)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
