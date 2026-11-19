# test/test_views.py
"""
Test d'API et d'intégration sur les EndPoints : 
    - EquipmentListView
    - EquipmentDetailView (get / put)
"""
import allure
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Equipment


@pytest.fixture
def api_client():
    """Retourne un client API DRF non authentifié."""
    return APIClient()

@pytest.fixture
def sample_item(db):
    """
    Crée un objet en base de données pour 
    les tests de lecture/modification.
    """
    return [
        Equipment.objects.create(
                    name = "MacBook Pro",
                    category = "Informatique",
                    is_available = True
                ),
        Equipment.objects.create(
                    name = "Ecran ACER 17''",
                    category = "Périphérique",
                    is_available = False
                )
    ]

@pytest.mark.django_db
@allure.epic("Application EquipIT - Gestion du parc matériel")
@allure.feature("API & Intégration des Endpoints")
class TestEquipementEndPoints:

    @allure.story("Récupération de la liste des Equipements")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_list_equipement(self, api_client, sample_item):
        """
            Vérifie qu'un utilisateur non authentifié 
            peut obtenir la liste des équiments
        """
        allure.dynamic.title("Récupération de la liste des équipements")
        allure.dynamic.description(
            "Fonctionnalité sans authentification."
            "Récupère la liste de tous les équipements"
        )
        with allure.step("1. Arrange : Initialisation de l'url"):
            url = reverse("equipment-list")
        with allure.step("2. Action : envoi de la requête "):
            response = api_client.get(url)
        with allure.step("3. Assert : évaluation des résultats"):
            assert response.status_code == status.HTTP_200_OK
            assert len(response.data) == 2
            assert response.data[0]["name"] == sample_item[0].name

    @allure.story("Affiche le détail d'un Equipement spécifique")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_equipement_details(self, api_client, sample_item):
        """
            Vérifie qu'il est possible d'obtenir le détail 
            d'un équipement spécifique
        """
        allure.dynamic.title("Affiche le détails d'un équipement spécifique")
        allure.dynamic.description(
            "Fonctionnalité sans authentification."
            "A partir de l'Id communiqué, affiche la liste des valeurs "
            "d'attribut d'un équipement"
        )
        with allure.step("1. Arrange : Initialisation de l'url"):
            url = reverse(
                    "equipment-detail", 
                    kwargs={"equipment_id": sample_item[0].id}
                )
        with allure.step("2. Action : envoi de la requête "):
            response = api_client.get(url)

        with allure.step("3. Assert : évaluation des résultats"):
            assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    @pytest.mark.parametrize(
        (
            "case_title","action_url", "equipment_id","is_available","payload", 
            "expected_item", "expected_detail"
        ),
        [
            (
                "Restitution nominale d'un équipement emprunté",
                "return", 2,False, {}, 
                status.HTTP_200_OK,""
            ),
            (
                "Restitution d'un équipement déjà retourné",
                "return", 1,True, {}, status.HTTP_400_BAD_REQUEST,""
            ),
            (
                "Restitution d'un équipement inexistant",
                "return", 11,False, 
                {},
                status.HTTP_404_NOT_FOUND,
                "Equipement inexistant"
            ),
            (
                "Emprunt nominal d'un équipement disponible",
                "borrow", 1,True, 
                {
                    "first_name": "Jean",
                    "last_name": "Dupont",
                }, status.HTTP_200_OK, ""
            ),
            (
                "Tentative d'emprunt d'un équipement déjà emprunté",
                "borrow", 2,False, 
                {
                    "first_name": "Jean",
                    "last_name": "Dupont",
                },
                status.HTTP_400_BAD_REQUEST,
                "Cet équipement est déjà emprunté"
            ),
            (
                "Tentative d'eumprunt d'un équipement inexistant",
                "borrow", 11,True, 
                {
                    "first_name": "Jean",
                    "last_name": "Dupont",
                },
                status.HTTP_404_NOT_FOUND,
                "Equipement inexistant"
            ),
            (
                (
                    "Tentative d'emprunt sans renseigner "
                    "les champs obligatoires First_name et last_name"
                ),
                "borrow", 1,True, 
                {},
                status.HTTP_400_BAD_REQUEST,
                "Ce champ est obligatoire."
            ),
        ]
    )
    @allure.story(
            "Evalue la fonction d'emprunt ou de "
            "restitution d'une Equipement"
        )
    @allure.severity(allure.severity_level.CRITICAL)
    def test_borrow_or_return_an_equipment(
                self, api_client, sample_item, case_title,
                action_url,equipment_id,is_available, payload,
                expected_item, expected_detail                              
            ):
        """
            Vérifie les endpoints sur les actions personnalisés 
            (empreunté / retourner) fonctionnent
        """
        allure.dynamic.title(case_title)
        allure.dynamic.description(
            f"Vérifie le comportement de l'action **{action_url}**"
            f" sur l'équipement #{equipment_id} "
            f"(état initial disponible={is_available})."
        )
        with allure.step("1. Arrange : Préparation de l'url"):
            url = reverse(
                    f"equipment-{action_url}", 
                    kwargs={"equipment_id": equipment_id}
                )  
            payload = payload
        with allure.step("2. Action : Envoi de la requête"):
            response = api_client.put(url, data=payload, format="json")
            
        with allure.step("1. Assert : Analyse des comportements"):
            assert response.status_code == expected_item

            if response.status_code == status.HTTP_200_OK:
                assert response.data["is_available"] is not is_available
                if action_url == "borrow":
                    assert (
                            response.data["borrower_first_name"] 
                            == payload["first_name"]
                        )
                    assert (
                            response.data["borrower_last_name"] 
                            == payload["last_name"]
                        )
            else :
                assert expected_detail in str(response.data)
