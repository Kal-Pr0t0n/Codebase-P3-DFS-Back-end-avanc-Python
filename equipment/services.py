from django.db import transaction
from django.utils import timezone

from .models import Equipment


class EquipmentNotFoundError(Exception):
    pass


class EquipmentUnavailableError(Exception):
    pass


class EquipmentAlreadyAvailableError(Exception):
    pass


class EquipmentService:
    def find_equipment(self, equipment_id: int) -> Equipment:
        try:
            return Equipment.objects.get(pk=equipment_id)
        except Equipment.DoesNotExist as exc:
            raise EquipmentNotFoundError("Equipement inexistant") from exc

    @transaction.atomic
    def borrow_equipment(
            self, equipment_id: int, first_name: str, last_name: str
        ) -> Equipment:
        equipment = self.find_equipment(equipment_id=equipment_id)
        if not equipment.is_available:  # Exemple de règle métier
            raise EquipmentUnavailableError("Cet équipement est déjà emprunté")

        equipment.borrower_first_name = first_name
        equipment.borrower_last_name = last_name
        equipment.borrowed_at = timezone.now()
        equipment.returned_at = None
        equipment.is_available = False
        equipment.save()

        return equipment

    @transaction.atomic
    def return_equipment(self, equipment_id: int) -> Equipment:
        equipment = self.find_equipment(equipment_id=equipment_id)
        if equipment.is_available :
            raise EquipmentAlreadyAvailableError(
                    "Cet équipement a déjà été retourné"
                )
        equipment.is_available = True
        equipment.returned_at = timezone.now()
        equipment.save()

        return equipment