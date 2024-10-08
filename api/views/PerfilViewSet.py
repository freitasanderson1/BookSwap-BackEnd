from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
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
        
    #seguir perfil
    @action(detail=True, methods=['POST'],permission_classes=[IsAuthenticated])
    def seguir(self,request,pk=None):
        perfil_a_seguir = get_object_or_404(Perfil,pk=pk)
        perfil_autenticado = request.user.perfil
        
        if perfil_autenticado.esta_seguindo(perfil_a_seguir):
            return Response({'detail':'Voce ja esta seguindo este perfil.'},status=status.HTTP_400_BAD_REQUEST)
        
        perfil_autenticado.seguir(perfil_a_seguir)
        return Response({'detail':'Agora voce esta seguindo este perfil.'},status=status.HTTP_200_OK)
    
    #unfollow perfil
    @action(detail=True,methods=['DELETE'],permission_classes=[IsAuthenticated])
    def deixar_de_seguir(self,request,pk=None):
        perfil_para_deixar = get_object_or_404(Perfil,pk=pk)
        perfil_autenticado = request.user.perfil
        
        if not perfil_autenticado.esta_seguindo(perfil_para_deixar):
            return Response({'detail':'Voce nao esta seguindo este perfil.'},status=status.HTTP_400_BAD_REQUEST)

        perfil_autenticado.deixar_de_seguir(perfil_para_deixar)
        return Response({'detail':'Voce deixou de seguir este perfil.'},status=status.HTTP_200_OK)