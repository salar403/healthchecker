from backend.customs.views import CreateApiView, RetrieveApiView, DestroyApiView
from drf_yasg.utils import swagger_auto_schema

from user.permissions import IsAuthenticated
from .serializers import (
    AddEndpointSerizlier,
    CallResultSerializer,
    HistoricalStateSerializer,
    ListEndpointSerializer,
    DeleteEndpointSerializer,
    LiveStateSerializer,
)


class AddEndpoint(CreateApiView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddEndpointSerizlier
    context_map = {"user": "customer"}


class ListEndpoints(RetrieveApiView):
    permission_classes = [IsAuthenticated]
    serializer_class = ListEndpointSerializer
    context_map = {"user": "customer"}

    @swagger_auto_schema(query_serializer=serializer_class)
    def get(self, request):
        return super().get(request)


class DeleteEndpoint(DestroyApiView):
    permission_classes = [IsAuthenticated]
    serializer_class = DeleteEndpointSerializer
    context_map = {"user": "customer"}

    @swagger_auto_schema(request_body=serializer_class)
    def delete(self, request):
        return super().delete(request)


class LiveStates(RetrieveApiView):
    permission_classes = [IsAuthenticated]
    serializer_class = LiveStateSerializer
    context_map = {"user": "customer"}

    @swagger_auto_schema(query_serializer=serializer_class)
    def get(self, request):
        return super().get(request)


class HistoricalStates(RetrieveApiView):
    permission_classes = [IsAuthenticated]
    serializer_class = HistoricalStateSerializer
    context_map = {"user": "customer"}

    @swagger_auto_schema(query_serializer=serializer_class)
    def get(self, request):
        return super().get(request)


class CallResults(RetrieveApiView):
    permission_classes = [IsAuthenticated]
    serializer_class = CallResultSerializer
    context_map = {"user": "customer"}

    @swagger_auto_schema(query_serializer=serializer_class)
    def get(self, request):
        return super().get(request)