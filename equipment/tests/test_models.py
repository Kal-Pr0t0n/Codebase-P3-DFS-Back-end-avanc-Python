# test/test_models.py
"""
Test Unitaires sur les models :
    - Equipment
"""

from django.test import TestCase
from django.utils import timezone

from ..models import Equipment


class EquipementModelTest(TestCase):
    def setUp(self):
        self.equipement = Equipment.objects.create(
            name = "MacBook Pro",
            category = "Informatique",
            is_available = True
        )

    def test_str_representation(self):
        self.assertEqual(str(self.equipement), "MacBook Pro")

    def test_borrow_business_logic(self):
        # Simulation d'une logic d'emprunt
        self.equipement.borrower_first_name = "Fabrice"
        self.equipement.borrower_last_name = "MAILLOT"
        self.equipement.is_available = False 
        self.equipement.borrowed_at = timezone.now()
        self.equipement.save()

        self.assertFalse(self.equipement.is_available)
        self.assertEqual(self.equipement.borrower_first_name, "Fabrice")
        self.assertIsNotNone(self.equipement.borrowed_at)