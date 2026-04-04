from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

User = get_user_model()

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not email or not password:
        return Response(
            {'error': 'Email y contraseña requeridos'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Try to find user by email
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(
            {'error': 'Credenciales incorrectas'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    # Authenticate with username
    user = authenticate(username=user.username, password=password)
    
    if user is not None:
        # Simple token (in production use proper JWT)
        return Response({
            'token': f'admin_token_{user.id}',
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username
            }
        })
    
    return Response(
        {'error': 'Credenciales incorrectas'},
        status=status.HTTP_401_UNAUTHORIZED
    )
