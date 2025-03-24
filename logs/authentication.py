from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        
        access_token = request.COOKIES.get("access_token")
        if not access_token:
            return super().authenticate(request) 
        
        try:
            validated_token = self.get_validated_token(access_token)
            user = self.get_user(validated_token)
            return (user, validated_token)  
        except Exception:
            raise AuthenticationFailed("Invalid or expired token")