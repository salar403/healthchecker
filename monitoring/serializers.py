from rest_framework import serializers
from backend.customs.queryset import get_object_or_404

from backend.customs.serializers import (
    PaginatedTimeFilteredSerializer,
    PaginatedSerializer,
)

from .models import CallResult, Endpoint


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
        endpoint.is_deleted = True
        endpoint.save()
        self._data = {"code": "success"}
        return True


class StateModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallResult
        fields = ["healthy", "timestamp"]

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["endpoint_id"] = instance.endpoint.id
        ret["endpoint_name"] = instance.endpoint.name
        return ret


class LiveEndpointStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endpoint
        fields = ["id", "name"]

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        last_call_result = instance.callresults.last()
        ret["last_state"] = last_call_result.healthy
        ret["last_timestamp"] = last_call_result.timestamp
        return ret


class LiveStateSerializer(serializers.Serializer):
    def to_representation(self, instance):
        super().to_representation(instance)
        endpoints = self.context["user"].endpoints.filter(is_deleted=False)
        return {
            "code": "success",
            "data": LiveEndpointStateSerializer(endpoints, many=True).data,
        }


class HistoricalStateSerializer(PaginatedSerializer):
    MODEL_SERIALIZER = StateModelSerializer
    ORDER_BY = "id"

    endpoint_id = serializers.IntegerField(required=True, min_value=1)

    def validate_endpoint_id(self, endpoint_id):
        self._endpoint = get_object_or_404(
            self.context["user"].endpoints, id=endpoint_id, is_deleted=False
        )
        return self._endpoint

    def get_queryset(self, filters: dict):
        return self._endpoint.call_results.filter(**filters).order_by(self.ORDER_BY)
