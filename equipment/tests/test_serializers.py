# test/test_serializers.py
"""
Test Unitaires sur les serializers : 
    - EquipmentSerializer
    - BorrowRequestSerializer
"""
import allure
from django.test import TestCase

from ..models import Equipment
from ..serializers import BorrowRequestSerializer, EquipmentSerializer


@allure.epic("Application EquipIT - Gestion du parc matériel")
@allure.feature("Test Unitaires de sérialisation")
class EquipmentSerializerTest(TestCase):
    @allure.story(
            "Serialisation des données à transmettre dans le flux "
            "d'API REST pour la liste d'équipement"
        )
    @allure.severity(allure.severity_level.BLOCKER)
    def setUp(self):
        self.equipement_attributes = {
            "name" : "Ecran Dell 27''",
            "category" : "Informatique",
            "is_available" : True
        }
        self.equipement = Equipment.objects.create(**self.equipement_attributes)

    def test_serializer_contain_expected_fields(self):
        """On vérifie que tous les champs attendus sont présents dans la sortie"""
        allure.dynamic.title("Vérification des champts de sortie")
        allure.dynamic.description(
            "On s'assure que les champs attendus sont bien présent"
            "dans la sortie de sérialisation"
        )

        with allure.step("1. Arrange and Action : Initialisation du serializer"):
            serializer = EquipmentSerializer(instance= self.equipement)
            expected_fields = [
                "id", "name", "category", "is_available", 
                "borrower_first_name", "borrower_last_name", 
                "borrowed_at", "returned_at"
            ]
        with allure.step("2. Assert : Evaluation des sortie"):
            self.assertEqual(
                set(serializer.data.keys()),
                set(expected_fields)
            )

    allure.dynamic.title("Compare les données de sortie au modèle")
    allure.dynamic.description(
        "On s'assure que les champs de sortie"
        " correspondent aux données initiales du modèle."
    )
    def test_serializer_field_content(self):
        """Vérifie que les valeurs sérialisées correspondent aux données du modééle."""
        with allure.step("1. Arrange and Action : Initialisation du serializer"):
            serializer = EquipmentSerializer(instance=self.equipement)
        with allure.step("2. Assert : Evaluation des données de sorties"):
            self.assertEqual(
                serializer.data["name"], self.equipement_attributes["name"]
            )
            self.assertEqual(
                serializer.data["category"], self.equipement_attributes["category"]
            )
            self.assertTrue(serializer.data["is_available"])

class BorrowRequestSerializer_quest(TestCase):
    @allure.story("Serialisation des données relatif à l'emprunt")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_valid_barrow_request(self):
        allure.dynamic.title("Analyse du Sérializer relatif à l'emprunt")
        allure.dynamic.description(
            "Analyse le sérializer relatif à l'appel de la fonction d'emprunt"
        )
        with allure.step("1. Arrange : Affectation des data"):
            valid_data = {
                "first_name" : "Fabrice",
                "last_name"  : "MAILLOT"
            }
        with allure.step("2. Action"):
            serilizer = BorrowRequestSerializer(data=valid_data)
        with allure.step("3. Evaluation des comportements"):
            self.assertTrue(
                serilizer.is_valid()
            )
            self.assertEqual(
                serilizer.validated_data,
                valid_data
            )

    @allure.story("Impacte des champs obligatoire")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_missing_requiered_fileds(self):
        allure.dynamic.title(
                "Vérifie le comportement lors de l'absence "
                "des champs obligatoires"
            )
        allure.dynamic.description(
            "Evaluation du comportement lorsqu'un champ obligatoire est omis."
        )
        """Vérifie que les champs obligatoires manquant déclenchent une erreur."""
        with allure.step("1. Initialisation des données éronnées"):
            invalid_data = {
                "first_name" : "Fabrice",
                # Last_name manquant
            }
        with allure.step("2. Action : appel du serializer"):
            serializer = BorrowRequestSerializer(data=invalid_data)
        with allure.step("3. Evaluation des comportements"):
            self.assertFalse(
                serializer.is_valid()
            )
            self.assertIn("last_name", serializer.errors)

    @allure.story("evalue le comportement lors du passage de champ vide")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_blank_field_not_allowed(self):
        """Vérifie que les champs vides ne sont pas acceptés"""
        allure.dynamic.title(
                "Vérifie que les champs vides ne sont pas acceptés"
            )
        allure.dynamic.description(
            "Vérifie que les champs vides ne sont pas acceptés"
            )
        with allure.step("1. Initialisation des valeurs éronénes"):
            invalid_data = {
                "first_name": "",
                "last_name": "Martin"
            }
        with allure.step("2. Action"):
            serializer = BorrowRequestSerializer(data=invalid_data)
        with allure.step("3. Assert : Evaluation des comportements"):
            self.assertFalse(serializer.is_valid())
            self.assertIn("first_name", serializer.errors)

    @allure.story("Vérifie que les limites de taille de champ est respecté")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_max_length_validation(self):
        """Vérifie le respect de la limite de taille maximale (max_length=80)."""
        invalid_data = {
            "first_name": "A" * 81,  # Dépasse 80 caractères
            "last_name": "Martin"
        }
        allure.dynamic.title(
            "Vérifie le respect de la limite de taille maximale (max_length=80)."
        )
        allure.dynamic.description(
            "Vérifie le respect de la limite de taille maximale (max_length=80)."
        )
        with allure.step("1. Arrange and Action"):
            serializer = BorrowRequestSerializer(data=invalid_data)
        with allure.step("2. Assert : Evaluation des comportements"):
            self.assertFalse(serializer.is_valid())
            self.assertIn("first_name", serializer.errors)