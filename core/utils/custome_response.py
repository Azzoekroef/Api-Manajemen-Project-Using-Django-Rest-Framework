from rest_framework.response import Response

class CustomResponse():
    def __init__(self, data=None, message=None):
        self.data = data
        self.message = message

    def response_success(self):
        response = {
            'status': 'success',
            'message': 'Data retriveing successfully',
            'data': self.data
        }
        return Response(response)

    def response_error(self):
        response = {
            'status': 'error',
            'message': self.message,
        }
        return Response(response)