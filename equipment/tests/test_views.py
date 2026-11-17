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
    """Crée un objet en base de données pour les tests de lecture/modification."""
    return Equipment.objects.create(
                    name = "MacBook Pro",
                    category = "Informatique",
                    is_available = True
                )

@pytest.mark.django_db
class TestEquipementEndPoints:

    def test_get_list_equipement(self, api_client, sample_item):
        """Vérifie qu'un utilisateur non authentifié peut obtenir la liste des équiments"""
        url = reverse("equipment-list")

        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["name"] == sample_item.name

    def test_get_equipement_details(self, api_client, sample_item):
        """Vérifie qu'il est possible d'obtenir le détail d'un équipement spécifique"""
        url = reverse("equipment-action", kwargs={"equipment_id": sample_item.id, "action":"get"})

        response = api_client.get(url)

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_add_an_equipment(self, api_client, sample_item):
        """Vérifie qu'il est possible  de modifier un équipement spécifique"""
        url = reverse("equipment-action", kwargs={"equipment_id": sample_item.id, "action":"put"})

        response = api_client.put(url)

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
