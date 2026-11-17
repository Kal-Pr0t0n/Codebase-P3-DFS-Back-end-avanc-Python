# test/test_services.py
"""
Test Unitaires sur les services : 
    - EquipmentService
"""
from contextlib import nullcontext as does_not_raise

import pytest

from ..models import Equipment
from ..services import (
    EquipmentNotFoundError,
    EquipmentService,
)


@pytest.fixture
def sample_item(db):
    """Crée un objet en base de données pour les tests de lecture/modification."""
    return Equipment.objects.create(
                    name = "MacBook Pro",
                    category = "Informatique",
                    is_available = True
                )

@pytest.mark.django_db
class TestEquipementService:
    @pytest.mark.parametrize(
            ("equipment_id", "expectation", "expected_item"),
            [
                (99, pytest.raises(EquipmentNotFoundError, match=None), None),
                (1, does_not_raise(), sample_item),
            ]
        )
    def test_if_equipment_not_exist(
                self, sample_item, equipment_id, 
                expectation, expected_item
            ):
        equipment_service = EquipmentService()
        with expectation:
            result = equipment_service.find_equipment(equipment_id=equipment_id)
            assert result.name == 'MacBook Pro'

    @pytest.mark.parametrize(
            ("equipment_id","is_available","username", "expectation", "expected_item"),
            [
                (
                    1, False, ("Ducon","JAIPAYE"), 
                    pytest.raises(NotImplementedError, match=None), None
                ), 
                (
                    1, True, ("Ducon","JAIPAYE"),  
                    pytest.raises(NotImplementedError, match=None), sample_item
                ),
            ]
        )
    def test_bowworw_equipment(
                self, equipment_id, is_available, username, 
                expectation, expected_item
            ):
        """Vérifie la fonction : emprunter un équipement"""
        equipment_service = EquipmentService()
        with expectation:
            result = equipment_service.borrow_equipment(
                    equipment_id=equipment_id, 
                    first_name=username[0], 
                    last_name=username[1]
                )
            assert result.name == 'MacBook Pro'

    @pytest.mark.parametrize(
            ("equipment_id","is_available", "expectation", "expected_item"),
            [
                (
                    1, False, 
                    pytest.raises(NotImplementedError, match=None), None
                ), 
                (
                    1, True,  
                    pytest.raises(NotImplementedError, match=None), sample_item
                ),
            ]
        )
    def test_return_equipment(
                self, equipment_id, is_available, expectation, expected_item
            ):
        """Vérifie la fonction : retourner un équipement"""
        equipment_service = EquipmentService()
        with expectation:
            result = equipment_service.return_equipment(
                    equipment_id=equipment_id
                )
            assert result.name == 'MacBook Pro'
    
            
