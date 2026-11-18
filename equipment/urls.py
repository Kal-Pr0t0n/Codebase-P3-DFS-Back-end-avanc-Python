
from django.urls import path

from .views import EquipmentBorrowView, EquipmentDetailView, EquipmentListView, EquipmentReturnView

urlpatterns = [
    path("equipment/", EquipmentListView.as_view(), name="equipment-list"),
    path(
        "equipment/<int:equipment_id>/",
        EquipmentDetailView.as_view(),
        name="equipment-detail",
    ),
    path(
        "equipment/<int:equipment_id>/borrow/",
        EquipmentBorrowView.as_view(),
        name="equipment-borrow",
    ),
    path(
        "equipment/<int:equipment_id>/return/",
        EquipmentReturnView.as_view(),
        name="equipment-return",
    ),
]
