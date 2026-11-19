from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import generics, status
from rest_framework.response import Response

from equipment.services import EquipmentAlreadyAvailableError

from .models import Equipment
from .serializers import BorrowRequestSerializer, EquipmentSerializer
from .services import EquipmentNotFoundError, EquipmentService, EquipmentUnavailableError


class EquipmentListView(generics.ListAPIView):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer


class EquipmentDetailView(generics.GenericAPIView):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer

class EquipmentReturnView(generics.GenericAPIView):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer

    @extend_schema(
        summary="Rapporter un équipement",
        request=None,  # Indique à Swagger qu'aucun body JSON n'est attendu en entrée
        responses={
            200: EquipmentSerializer,
            400: OpenApiResponse(description="Données invalides ou équipement déjà retourné."),
            404: OpenApiResponse(description="Équipement introuvable."),
        },
    )

    def put(self, request, equipment_id):
        """
        Endpoint personnalisé : PUT /api/equipment/{equipment_id}/return/
        """
        service = EquipmentService()
        try:
            equipement = service.return_equipment(equipment_id)
        except EquipmentNotFoundError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_404_NOT_FOUND)
        except EquipmentAlreadyAvailableError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        serializer = EquipmentSerializer(equipement)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EquipmentBorrowView(generics.GenericAPIView):
    queryset = Equipment.objects.all()
    serializer_class = BorrowRequestSerializer

    @extend_schema(
        summary="Emprunter un équipement",
        description="Assigne un équipement disponible à un utilisateur via son prénom et son nom.",
        request=BorrowRequestSerializer,  # Génère les champs first_name et last_name dans Swagger
        responses={
            200: EquipmentSerializer,
            400: OpenApiResponse(description="Données invalides ou équipement déjà emprunté."),
            404: OpenApiResponse(description="Équipement introuvable."),
        },
    )

    def put(self, request, equipment_id):
        """
        Endpoint personnalisé : PUT /api/equipment/{equipment_id}/borrow/
        """
        input_serializer = self.get_serializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        service = EquipmentService()

        try:
            equipment = service.borrow_equipment(
                equipment_id=equipment_id,
                first_name=input_serializer.validated_data["first_name"],
                last_name=input_serializer.validated_data["last_name"],
            )
        except EquipmentNotFoundError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_404_NOT_FOUND)
        except EquipmentUnavailableError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        # 3. Sérialisation de l'objet Equipment mis à jour pour la réponse
        serializer = EquipmentSerializer(equipment)
        return Response(serializer.data, status=status.HTTP_200_OK)