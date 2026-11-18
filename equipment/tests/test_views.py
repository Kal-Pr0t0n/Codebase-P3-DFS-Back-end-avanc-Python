# test/test_views.py
"""
Test d'API et d'intégration sur les EndPoints : 
    - EquipmentListView
    - EquipmentDetailView (get / put)
"""

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
class TestEquipementEndPoints:

    def test_get_list_equipement(self, api_client, sample_item):
        """
            Vérifie qu'un utilisateur non authentifié 
            peut obtenir la liste des équiments
        """
        url = reverse("equipment-list")

        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        assert response.data[0]["name"] == sample_item[0].name

    def test_get_equipement_details(self, api_client, sample_item):
        """
            Vérifie qu'il est possible d'obtenir le détail 
            d'un équipement spécifique
        """
        url = reverse(
                "equipment-detail", 
                kwargs={"equipment_id": sample_item[0].id}
            )

        response = api_client.get(url)

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    @pytest.mark.parametrize(
        (
            "action_url", "equipment_id","is_available","payload", 
            "expected_item", "expected_detail"
        ),
        [
            (
                "return", 2,False, {}, 
                status.HTTP_200_OK,""
            ),
            (
                "return", 1,True, {}, status.HTTP_400_BAD_REQUEST,""
            ),
            (
                "return", 11,False, 
                {},
                status.HTTP_404_NOT_FOUND,
                "Equipement inexistant"
            ),
            (
                "borrow", 1,True, 
                {
                    "first_name": "Jean",
                    "last_name": "Dupont",
                }, status.HTTP_200_OK, ""
            ),
            (
                "borrow", 2,False, 
                {
                    "first_name": "Jean",
                    "last_name": "Dupont",
                },
                status.HTTP_400_BAD_REQUEST,
                "Cet équipement est déjà emprunté"
            ),
            (
                "borrow", 11,True, 
                {
                    "first_name": "Jean",
                    "last_name": "Dupont",
                },
                status.HTTP_404_NOT_FOUND,
                "Equipement inexistant"
            ),
            (
                "borrow", 1,True, 
                {},
                status.HTTP_400_BAD_REQUEST,
                "Ce champ est obligatoire."
            ),
        ]
    )
    def test_borrow_or_return_an_equipment(
                self, api_client, sample_item,
                action_url,equipment_id,is_available, payload,
                expected_item, expected_detail                              
            ):
        """
            Vérifie les endpoints sur les actions personnalisés 
            (empreunté / retourner) fonctionnent
        """
        url = reverse(
                f"equipment-{action_url}", 
                kwargs={"equipment_id": equipment_id}
            )  
        payload = payload
        response = api_client.put(url, data=payload, format="json")
        
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
