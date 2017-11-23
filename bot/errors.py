from django.http import JsonResponse, Http404

class OTError(Exception):
    def __init__(self, code, message, http_code=200):
        self.code = code
        self.message = message
        self.http_code = http_code

    def __str__(self):
        return "ERROR: ({0}:{1}) {2}".format(self.http_code, self.code, self.message)

    def to_response(self) -> JsonResponse:
        return error_response(self.code, self.message, self.http_code)


class OTNotImplementedError(OTError):
    def __init__(self, message='Not implemented'):
        OTError.__init__(self, OT_ERROR_NOT_IMPLEMENTED, message, 500)


def error_response(code: int, message: str, http_code: int = 200):
    return JsonResponse(
        {
            'ok': False,
            'error_code': code,
            'error_message': message,
        },
        status=http_code
    )


def success_response(data: dict=dict(), http_code: int = 200):
    return JsonResponse(
        { **{'ok': True}, **data},
        status=http_code
    )

def empty_success_response(data: dict=dict(), http_code: int = 200):
    return JsonResponse(
        { **{"":""}, **data},
        status=http_code
    )

# This guy handles all API errors
def custom_exception_handler(exc, context):
    if type(exc) is OTError:
        return exc.to_response()
    status_code = 500

    if type(exc) is Http404:
        status_code = 404

    if hasattr(exc, 'status_code'):
        status_code = exc.status_code

    return error_response(OT_ERROR_INTERNAL_ERROR, "Error: " + str(exc), status_code)


# Error constants
OT_ERROR_NOT_IMPLEMENTED = 1100
OT_ERROR_UNAUTHORIZED = 1401
OT_ERROR_FORBIDDEN = 1403
OT_ERROR_BACKEND_ERROR = 1505
OT_ERROR_INTERNAL_ERROR = 1500
