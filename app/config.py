import os

class Config:
    TITLE = os.getenv("TITLE", "Default Title")
    RESPONSE_TIME = int(os.getenv("RESPONSE_TIME", 0))
    EXTERNAL_CALL_URL = os.getenv("EXTERNAL_CALL_URL", "")
    EXTERNAL_CALL_METHOD = os.getenv("EXTERNAL_CALL_METHOD", "GET")
    HTTP_PORT = int(os.getenv("HTTP_PORT", 5000))