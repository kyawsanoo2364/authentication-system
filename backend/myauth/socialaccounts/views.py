from rest_framework.generics import GenericAPIView
from .serializers import GoogleAPISerializer
from rest_framework.response import Response


class GoogleApiView(GenericAPIView):
    serializer_class = GoogleAPISerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            return Response(
                {"data": data, "message": "Log in successfully"}, status=200
            )
        return Response({serializer.errors}, status=400)
