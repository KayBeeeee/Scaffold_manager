from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from decimal import Decimal


class ScaffoldComponent(models.Model):
    CATEGORY_CHOICES = [
        ("Tube", "Tube"),
        ("Board", "Board"),
        ("Coupler", "Coupler"),
        ("Jack", "Jack"),
        ("Frame", "Frame"),
        ("Other", "Other"),
    ]

    CONDITION_CHOICES = [
        ("NEW", "NEW"),
        ("GOOD", "GOOD"),
        ("REPAIR", "REPAIR"),
        ("SCRAP", "SCRAP"),
    ]

    SITE_CHOICES = [
        ("Secunda", "Secunda"),
        ("Sasolburg", "Sasolburg"),
    ]

    asset_code = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    length_mm = models.IntegerField(null=True, blank=True)
    weight_kg = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, default="GOOD")
    site = models.CharField(max_length=20, choices=SITE_CHOICES)
    location = models.CharField(max_length=100, null=True, blank=True)
    last_inspection = models.DateField()
    next_inspection = models.DateField()
    is_in_use = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("asset_code", "site")
        # default ordering is handled in ListView using explicit ordering (so no reliance on alphabetical)
        verbose_name = "Scaffold Component"
        verbose_name_plural = "Scaffold Components"

    def clean(self):
        errors = {}
        if self.weight_kg is not None and self.weight_kg <= 0:
            errors["weight_kg"] = "weight_kg must be greater than zero."
        if self.length_mm is not None and not (1 <= self.length_mm <= 6000):
            errors["length_mm"] = "length_mm must be between 1 and 6000 if provided."
        if self.last_inspection and self.next_inspection and self.next_inspection < self.last_inspection:
            errors["next_inspection"] = "next_inspection must be greater than or equal to last_inspection."
        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return f"{self.asset_code} — {self.name}"
