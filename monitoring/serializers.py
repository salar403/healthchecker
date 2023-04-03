from rest_framework import serializers
from backend.customs.queryset import get_object_or_404

from backend.customs.serializers import PaginatedTimeFilteredSerializer
from backend.customs.exceptions import CustomException

from .models import Endpoint


class EndpointModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endpoint
        fields = "__all__"


class AddEndpointSerizlier(serializers.Serializer):
    name = serializers.CharField(required=True)
    base_url = serializers.URLField(required=True)
    method = serializers.CharField(required=True)
    timeout = serializers.IntegerField(required=True)
    check_interval = serializers.IntegerField(required=True)
    convert_body_to_json = serializers.BooleanField(allow_null=False, default=False)
    headers = serializers.JSONField(required=False)
    body = serializers.JSONField(required=False)
    query_params = serializers.JSONField(required=False)
    healthy_status_code = serializers.IntegerField(required=False)
    required_result = serializers.JSONField(required=False)

    def validate(self, data):
        for key in list(data):
            if key not in self.fields:
                data.pop(key)
        return data

    def create(self, validated_data):
        endpoint = Endpoint.objects.create(**validated_data)
        self._data = {"code": "success", "data": EndpointModelSerializer(endpoint).data}
        return super().create(validated_data)


class ListEndpointSerializer(PaginatedTimeFilteredSerializer):
    MODEL_SERIALIZER = EndpointModelSerializer
    ORDER_BY = "id"

    def get_queryset(self, filters: dict):
        return self.context["user"].endpoints.filter(**filters).order_by(self.ORDER_BY)


class DeleteEndpointSerializer(serializers.Serializer):
    endpoint_id = serializers.IntegerField(required=True, min_value=1)

    def validate_service_id(self, service_id):
        return get_object_or_404(
            self.context["user"].endpoints, id=service_id, is_active=True
        )

    def create(self, validated_data):
        endpoint = validated_data["endpoint_id"]
        endpoint.is_active = False
        endpoint.save()
        self._data = {"code": "success"}
        return True
