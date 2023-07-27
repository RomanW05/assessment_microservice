from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import ugettext_lazy as _

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Customize the token payload with additional claims (scopes)
        # In this example, we set the scope to 'restricted'
        token['scope'] = 'restricted'

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        # Customize the response data with additional claims (scopes)
        data['scope'] = 'restricted'

        return data

