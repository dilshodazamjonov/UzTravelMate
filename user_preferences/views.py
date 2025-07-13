from rest_framework.views import APIView
from rest_framework.response import Response
from user_preferences.models import Interest, TravelDestinations
from user_preferences.serializers import PreferencesChoicesSerializer
from user_preferences.serializers import InterestSerializer, TravelDestinationSerializer
from drf_yasg.utils import swagger_auto_schema

class InterestListView(APIView):
    permission_classes = []

    @swagger_auto_schema(responses={200: InterestSerializer(many=True)})
    def get(self, request):
        interests = Interest.objects.all().order_by('name')
        serializer = InterestSerializer(interests, many=True)
        return Response(serializer.data)
    
class TravelDestinationsListView(APIView):
    def get(self, request):
        destinations = TravelDestinations.objects.all()
        serializer = TravelDestinationSerializer(destinations, many=True)
        return Response(serializer.data)
    
class PreferencesChoicesView(APIView):
    permission_classes = []

    @swagger_auto_schema(
        operation_summary="Get travel style and budget level choices",
        responses={200: PreferencesChoicesSerializer}
    )
    def get(self, request):
        data = PreferencesChoicesSerializer.get_data()
        return Response(data)