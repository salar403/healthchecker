from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class CreateApiView(APIView):
    serializer_class = None
    permission_classes = []
    context_map = {}
    response_code = status.HTTP_201_CREATED

    def get_context(self):
        context = {}
        for key in self.context_map:
            context[key] = (
                getattr(self.request, self.context_map[key])
                if key != "request"
                else self.request
            )
        return context

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.serializer_class
        return serializer_class(*args, **kwargs)

    def post(self, request):
        serializer = self.get_serializer(data=request.data, context=self.get_context())
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=self.response_code)


class DestroyApiView(APIView):
    serializer_class = None
    permission_classes = []
    context_map = {}
    response_code = status.HTTP_204_NO_CONTENT

    def get_context(self):
        context = {}
        for key in self.context_map:
            context[key] = (
                getattr(self.request, self.context_map[key])
                if key != "request"
                else self.request
            )
        return context

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.serializer_class
        return serializer_class(*args, **kwargs)

    def delete(self, request):
        serializer = self.get_serializer(data=request.data, context=self.get_context())
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=self.response_code)


class RetrieveApiView(APIView):
    serializer_class = None
    permission_classes = []
    context_map = {}

    def get_context(self):
        context = {}
        for key in self.context_map:
            context[key] = (
                getattr(self.request, self.context_map[key], None)
                if key != "request"
                else self.request
            )
        return context

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.serializer_class
        return serializer_class(*args, **kwargs)

    def get(self, request):
        serializer = self.get_serializer(
            data=request.query_params,
            context=self.get_context(),
        )
        serializer.is_valid(raise_exception=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
