# test/test_services.py
"""
Test Unitaires sur les services : 
    - EquipmentService
"""
import allure
from contextlib import nullcontext as does_not_raise

import pytest

from ..models import Equipment
from ..services import (
    EquipmentAlreadyAvailableError,
    EquipmentNotFoundError,
    EquipmentService,
    EquipmentUnavailableError,
)

@allure.epic("Application EquipIT - Gestion du parc matériel")
@allure.feature("Test Unitaires sur les services")


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
    @allure.story("Fonctionnalité appliquées aux équipements")
    @allure.severity(allure.severity_level.BLOCKER)
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
        allure.dynamic.title("Comportement du service si l'équipement n'existe pas")
        allure.dynamic.description(
            "Evaluation du comportement du service dans le contexte"
            " où l'équipement n'existe pas."
        )
        with allure.step("1. Arrange and Action : appel du service"):
            equipment_service = EquipmentService()
        with (expectation):
            with allure.step(
                "2. Action: Appel de la fonction de recherche d'un équipement"
                ):
                result = equipment_service.find_equipment(equipment_id=equipment_id)
            with allure.step("3. Assert : Analyse du comportement"):
                assert result.name == 'MacBook Pro'

    @pytest.mark.parametrize(
            (
                "equipment_id","is_available","username", 
                "expectation", "expected_item"
            ),
            [
                (
                    1, False, ("Ducon","JAIPAYE"), 
                    pytest.raises(
                            EquipmentUnavailableError, 
                            match="Cet équipement est déjà emprunté"
                        ), None
                ), 
                (
                    1, True, ("Ducon","JAIPAYE"),  
                    does_not_raise(), sample_item
                ),
            ]
        )
    def test_bowworw_equipment(
                self, sample_item, equipment_id, is_available, username, 
                expectation, expected_item
            ):
        """Vérifie la fonction : emprunter un équipement"""
        allure.dynamic.title("Simule l'emprunt d'un équipement")
        allure.dynamic.description(
            "Evaluation du comportement du service lors des différents cas d'emprunt"
        )
        equipment_service = EquipmentService()
        equipment = equipment_service.find_equipment(equipment_id=equipment_id)
        equipment.is_available = is_available
        equipment.save()
        with expectation:
            result = equipment_service.borrow_equipment(
                    equipment_id=equipment_id, 
                    first_name=username[0], 
                    last_name=username[1]
                )
            assert result.name == 'MacBook Pro'
            assert result.is_available != is_available

    @pytest.mark.parametrize(
            ("equipment_id","is_available", "expectation", "expected_item"),
            [
                (
                    1, False, 
                    does_not_raise(), sample_item
                ), 
                (
                    1, True,  
                    pytest.raises(
                            EquipmentAlreadyAvailableError, 
                            match="Cet équipement a déjà été retourné"
                        ), None
                ),
            ]
        )
    def test_return_equipment(
                self, sample_item,equipment_id, is_available, 
                expectation, expected_item
            ):
        """Vérifie la fonction : retourner un équipement"""
        equipment_service = EquipmentService()
        equipment = equipment_service.find_equipment(equipment_id=equipment_id)
        equipment.is_available = is_available
        equipment.save()
        with expectation:
            result = equipment_service.return_equipment(
                    equipment_id=equipment_id
                )
            assert result.name == 'MacBook Pro'
            assert result.is_available != is_available
    