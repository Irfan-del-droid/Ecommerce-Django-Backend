from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    # Call standard DRF exception handler first
    response = exception_handler(exc, context)

    # Standardize error response
    if response is not None:
        custom_data = {
            'status': 'error',
            'message': response.data.get('detail', 'A server error occurred.'),
            'errors': response.data
        }
        
        # Consistent with Node.js backend: only include errors if detail is not the only field
        if 'detail' in response.data and len(response.data) == 1:
            del custom_data['errors']
            
        response.data = custom_data
    else:
        # Handle unhandled errors (500)
        return Response({
            'status': 'error',
            'message': str(exc) if hasattr(exc, 'message') else 'Internal Server Error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return response
