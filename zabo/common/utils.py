from api.users.serializers import ZabouserSerializer


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': ZabouserSerializer(user, context={'request': request}).data
    }
