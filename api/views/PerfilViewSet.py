from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from api.models import Perfil
from api.serializers import PerfilSerializer, PerfilCreateUpdateSerializer

class PerfilViewSet(viewsets.ModelViewSet):
    queryset = Perfil.objects.all()  # Define a generic queryset
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        # Use a different serializer for create, update, partial_update
        if self.action in ['update', 'partial_update']:
            return PerfilCreateUpdateSerializer
        return PerfilSerializer

    def get_object(self):
        # Retrieve profile by the ID provided in the URL, if available
        if self.kwargs.get('pk'):  # Check if 'pk' is in the URL
            return get_object_or_404(Perfil, pk=self.kwargs['pk'])
        # If no 'pk' is provided, return the profile of the authenticated user
        queryset = self.get_queryset().filter(usuario=self.request.user)
        return get_object_or_404(queryset)

    def perform_update(self, serializer):
        # Log to verify what is being sent
        print("Request FILES: ", self.request.FILES)
        print("Request DATA: ", self.request.data)

        # Save the profile and the image
        serializer.save()
