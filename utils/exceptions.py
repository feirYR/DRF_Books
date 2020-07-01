from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework import status
def custom_exception_handler(exc,context):
    error="%s %s %s" %(context['view'],context['request'].method,exc)
    print(error)
    response=exception_handler(exc,context)
    if response is None:
        return Response(
            {'message':'程序内部错误'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,exception=None
        )
    return response

