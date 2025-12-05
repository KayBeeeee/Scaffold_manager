from django.test import TestCase
from .models import ScaffoldComponent
from django.urls import reverse
from datetime import date, timedelta
from decimal import Decimal
from django.db.utils import IntegrityError

class ModelValidationTests(TestCase):
    def setUp(self):
        self.base = {
            "asset_code": "A1",
            "name": "Tube 6m",
            "category": "Tube",
            "length_mm": 6000,
            "weight_kg": Decimal("10.00"),
            "condition": "GOOD",
            "site": "Secunda",
            "last_inspection": date.today(),
            "next_inspection": date.today() + timedelta(days=30),
            "is_in_use": False,
        }

    def test_weight_must_be_positive(self):
        data = self.base.copy()
        data["weight_kg"] = Decimal("0")
        obj = ScaffoldComponent(**data)
        with self.assertRaises(Exception):
            obj.full_clean()

    def test_next_inspection_must_be_after_last(self):
        data = self.base.copy()
        data["next_inspection"] = date.today() - timedelta(days=1)
        obj = ScaffoldComponent(**data)
        with self.assertRaises(Exception):
            obj.full_clean()

    def test_unique_asset_code_per_site(self):
        ScaffoldComponent.objects.create(**self.base)
        data = self.base.copy()
        data["name"] = "Other"
        with self.assertRaises(IntegrityError):
            ScaffoldComponent.objects.create(**data)

class ListViewTests(TestCase):
    def setUp(self):
        ScaffoldComponent.objects.create(
            asset_code="A1", name="Tube1", category="Tube", weight_kg=Decimal("1.00"),
            last_inspection=date.today(), next_inspection=date.today(), site="Secunda",
        )
        ScaffoldComponent.objects.create(
            asset_code="B1", name="Board1", category="Board", weight_kg=Decimal("2.00"),
            last_inspection=date.today(), next_inspection=date.today(), site="Sasolburg",
        )

    def test_q_filter(self):
        resp = self.client.get(reverse("assets:list"), {"q": "Tube1"})
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Tube1")

    def test_site_filter(self):
        resp = self.client.get(reverse("assets:list"), {"site": "Secunda"})
        self.assertContains(resp, "Tube1")
        self.assertNotContains(resp, "Board1")
