from rest_framework import status
from rest_framework.exceptions import APIException


class AMSException(APIException):
    message = "A server error has occurred."
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, http_status=None, message=None, success=None):

        success = False
        message = AMSException.message if (message is None) else message
        http_status = AMSException.status_code if (http_status is None) else http_status

        detail = {
            "http_status": http_status,
            "message": message,
            "success": success,
        }

        super().__init__(detail, code=http_status)
