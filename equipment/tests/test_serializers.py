# test/test_serializers.py
"""
Test Unitaires sur les serializers : 
    - EquipmentSerializer
    - BorrowRequestSerializer
"""

from django.test import TestCase

from ..models import Equipment
from ..serializers import BorrowRequestSerializer, EquipmentSerializer


class EquipmentSerializerTest(TestCase):
    def setUp(self):
        self.equipement_attributes = {
            "name" : "Ecran Dell 27''",
            "category" : "Informatique",
            "is_available" : True
        }
        self.equipement = Equipment.objects.create(**self.equipement_attributes)

    def test_serializer_contain_expected_fields(self):
        """On vérifie que tous les champs attendus sont présents dans la sortie"""
        serializer = EquipmentSerializer(instance= self.equipement)
        expected_fields = [
            "id", "name", "category", "is_available", 
            "borrower_first_name", "borrower_last_name", 
            "borrowed_at", "returned_at"
        ]
        self.assertEqual(
            set(serializer.data.keys()),
            set(expected_fields)
        )

    def test_serializer_field_content(self):
        """Vérifie que les valeurs sérialisées correspondent aux données du modééle."""
        serializer = EquipmentSerializer(instance=self.equipement)
        self.assertEqual(
            serializer.data["name"], self.equipement_attributes["name"]
        )
        self.assertEqual(
            serializer.data["category"], self.equipement_attributes["category"]
        )
        self.assertTrue(serializer.data["is_available"])

class BorrowRequestSerializer_quest(TestCase):
    def test_valid_barrow_request(self):
        valid_data = {
            "first_name" : "Fabrice",
            "last_name"  : "MAILLOT"
        }
        serilizer = BorrowRequestSerializer(data=valid_data)
        self.assertTrue(
            serilizer.is_valid()
        )
        self.assertEqual(
            serilizer.validated_data,
            valid_data
        )

    def test_missing_requiered_fileds(self):
        """Vérifie que les champs obligatoires manquant déclenchent une erreur."""
        invalid_data = {
            "first_name" : "Fabrice",
            # Last_name manquant
        }
        serializer = BorrowRequestSerializer(data=invalid_data)
        self.assertFalse(
            serializer.is_valid()
        )
        self.assertIn("last_name", serializer.errors)

    def test_blank_field_not_allowed(self):
        """Vérifie que les champs vides ne sont pas acceptés"""
        invalid_data = {
            "first_name": "",
            "last_name": "Martin"
        }
        serializer = BorrowRequestSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("first_name", serializer.errors)

    def test_max_length_validation(self):
        """Vérifie le respect de la limite de taille maximale (max_length=80)."""
        invalid_data = {
            "first_name": "A" * 81,  # Dépasse 80 caractères
            "last_name": "Martin"
        }
        serializer = BorrowRequestSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("first_name", serializer.errors)