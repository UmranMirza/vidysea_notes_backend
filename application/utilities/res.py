
from fastapi import HTTPException,status
from fastapi.responses import JSONResponse




class APIResponse:
    def __init__(self, message, data=None, status=status.HTTP_200_OK, meta=None):
        self.payload = {
            "status": True,
            "data": data if data else {},
            "message": message,
            "type": "success",
            "httpStatusCode": status,
        }
        self.status = status
        self.headers = {"mimetype" : "application/json",
                  "content-type": "application/json" 
                }
    def to_json(self):     
        return JSONResponse(content=self.payload, status_code=self.status,headers=self.headers)


class APIError:
    def __init__(self, message, data=None, status=status.HTTP_500_INTERNAL_SERVER_ERROR):
        self.payload = {
            "status": False,
            "data": data if data else {},
            "message": message,
            "type": "fail",
            "httpStatusCode": status,
        }
        self.headers = {"mimetype" : "application/json",
                  "content-type": "application/json" 
                }
        self.status = status 
    def to_json(self):     
        return JSONResponse(content=self.payload, status_code=self.status,headers=self.headers)


