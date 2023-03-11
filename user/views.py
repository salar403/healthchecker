from backend.customs.views import (
    CreateApiView,
    APIView,
    Response,
    status,
)

from drf_yasg.utils import swagger_auto_schema

from user.serializers import UserLoginSerializer
from user.permissions import IsAuthenticated
from backend.environments import API_HOST


class UserLogin(APIView):
    @swagger_auto_schema(request_body=UserLoginSerializer)
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = Response(data=serializer.data, status=status.HTTP_200_OK)
        response.set_cookie(
            key="Bearer",
            value=response.data["token"],
            expires=None,
            domain=API_HOST,
            httponly=True,
            samesite="strict",
        )
        return response


class UserLogout(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema()
    def delete(self, request):
        request.session_obj.is_active = False
        request.session_obj.save()
        return Response(data={"code": "success"}, status=status.HTTP_204_NO_CONTENT)
