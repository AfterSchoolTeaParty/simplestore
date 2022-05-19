import settings
import requests
from datetime import datetime

requests.post(f"{settings.DATABASE_API_URL}/files", {
    "name" : "mantap",
    "extension" : "txt",
    "storage" : "mantap_jiwa",
    "uploaded" : datetime.now().timestamp()
})