from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import FastAPI, Request, status, Form, File, UploadFile
from starlette.exceptions import HTTPException as StarletteHTTPException


def mount_static(app):
    app.mount("/assets", StaticFiles(directory="templates/assets"), name="assets")
    app.mount(
        "/category/assets", StaticFiles(directory="templates/assets"), name="assets"
    )


app = FastAPI()
mount_static(app)
templates = Jinja2Templates(directory="templates")


@app.exception_handler(StarletteHTTPException)
async def my_custom_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return templates.TemplateResponse(
            "error.html",
            {
                "request": request,
                "code": "404",
                "detail": "The requested resource couldn't be found.",
            },
        )
    elif exc.status_code == 500:
        return templates.TemplateResponse(
            "error.html", {"request": request, "code": "500", "detail": exc.detail}
        )
    else:
        return templates.TemplateResponse(
            "error.html", {"request": request, "code": "Error", "detail": exc.detail}
        )
