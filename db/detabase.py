import os
from pathlib import Path
from dotenv import load_dotenv

import cloudinary
from deta import Deta


load_dotenv()
deta = Deta(os.getenv("deta_token"))
db_document = deta.Base(os.getenv("detabase_name"))

# authenticate cloudinary
cloudinary.config(
    cloud_name=os.getenv("cloud_name"),
    api_key=os.getenv("api_key"),
    api_secret=os.getenv("api_secret"),
    secure=True,
)
