from rest_framework import serializers


class PaginatedSerializer(serializers.Serializer):
    MODEL = None
    MODEL_SERIALIZER = None
    DEFAULT_FIELD_TO_FILTER_MAP = {}
    CUSTOM_FIELD_TO_FIELD_MAP = {}
    ORDER_BY = "-id"

    page = serializers.IntegerField(default=1, min_value=1)
    per_page = serializers.IntegerField(default=10, min_value=1, max_value=100)

    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)
        self._filters = {}
        self._starting_limit = 1
        self._ending_limit = 20

    def get_queryset(self, filters: dict):
        return self.MODEL.objects.filter(**filters).order_by(self.ORDER_BY)

    def get_paginated_queryset(self):
        self._base_queryset = self.get_queryset(filters=self._filters)
        self._total_result = self._base_queryset.count()
        return self._base_queryset[self._starting_limit : self._ending_limit]

    def config_pagination(self, data):
        self._page = data["page"]
        self._per_page = data["per_page"]
        self._starting_limit = (self._page - 1) * self._per_page
        self._ending_limit = self._page * self._per_page

    def config_field_mapping(self):
        self._field_mapping = (
            self.DEFAULT_FIELD_TO_FILTER_MAP | self.CUSTOM_FIELD_TO_FIELD_MAP
        )

    def config_filters(self, data):
        self.config_field_mapping()
        for field in self.fields:
            if field in ["page", "per_page"]:
                continue
            if not self.fields[field].required and field not in data:
                continue
            validator = getattr(self, f"_{field}_validator", None)
            value = validator(data[field]) if validator else data[field]
            if value or self.fields[field].allow_null:
                if field not in self._field_mapping:
                    self._filters[field] = value
                else:
                    self._filters[self._field_mapping[field]] = value

    def validate(self, data):
        self.config_pagination(data=data)
        self.config_filters(data=data)
        return data

    def get_serialized_data(self):
        queryset = self.get_paginated_queryset()
        return self.MODEL_SERIALIZER(queryset, many=True).data

    def to_representation(self, instance):
        serialized_data = self.get_serialized_data()
        return {
            "code": "success",
            "data": serialized_data,
            "page": self._page,
            "per_page": self._per_page,
            "total": self._total_result,
        }


class PaginatedTimeFilteredSerializer(PaginatedSerializer):
    FIELD_TO_FILTER_MAP = {"from_date": "created_at__gte", "to_date": "created_at__lte"}

    from_date = serializers.DateTimeField(required=False)
    to_date = serializers.DateTimeField(required=False)
