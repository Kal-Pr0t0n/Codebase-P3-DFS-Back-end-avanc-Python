# test/test_models.py
"""
Test Unitaires sur les models :
    - Equipment
"""
import allure
from django.test import TestCase
from django.utils import timezone

from ..models import Equipment

@allure.epic("Application EquipIT - Gestion du parc matériel")
@allure.feature("Test Unitaires sur le Modèle de données")

@allure.story("Evaluation des données en base")
@allure.severity(allure.severity_level.BLOCKER)
class EquipementModelTest(TestCase):

    def setUp(self):
        with allure.step("1. Arrange : Création des données fictives en db de test"):
            self.equipement = Equipment.objects.create(
                name = "MacBook Pro",
                category = "Informatique",
                is_available = True
            )


    def test_str_representation(self):
        with allure.step("2. Act and Assert : Evalue l'appe d'un Element"):
            self.assertEqual(str(self.equipement), "MacBook Pro")

    @allure.story("Evaluation du changement d'état des valeurs")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_borrow_business_logic(self):
        # Simulation d'une logic d'emprunt
        with allure.step("1. Arrange : Simulation de données d'emprunt"):
            self.equipement.borrower_first_name = "Fabrice"
            self.equipement.borrower_last_name = "MAILLOT"
            self.equipement.is_available = False 
            self.equipement.borrowed_at = timezone.now()
        with allure.step("2. Action : enregistrement de l'élément"):
            self.equipement.save()

        with allure.step("3. Assert : Evaluation des comportements"):
            self.assertFalse(self.equipement.is_available)
            self.assertEqual(self.equipement.borrower_first_name, "Fabrice")
            self.assertIsNotNone(self.equipement.borrowed_at)