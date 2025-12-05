from django import forms
from django.core.exceptions import ValidationError
from .models import ScaffoldComponent


class ScaffoldComponentForm(forms.ModelForm):
    class Meta:
        model = ScaffoldComponent
        fields = [
            "asset_code", "name", "category", "length_mm", "weight_kg",
            "condition", "site", "location", "last_inspection",
            "next_inspection", "is_in_use"
        ]
        widgets = {
            "last_inspection": forms.DateInput(
                attrs={"type": "date", "placeholder": "YYYY-MM-DD"},
                format="%Y-%m-%d"
            ),
            "next_inspection": forms.DateInput(
                attrs={"type": "date", "placeholder": "YYYY-MM-DD"},
                format="%Y-%m-%d"
            ),
        }

    def clean_weight_kg(self):
        weight = self.cleaned_data.get("weight_kg")
        if weight is None or weight <= 0:
            raise ValidationError("Weight must be greater than 0.")
        return weight

    def clean_length_mm(self):
        length = self.cleaned_data.get("length_mm")
        if length is not None and (length < 1 or length > 6000):
            raise ValidationError("Length must be between 1 and 6000 mm.")
        return length

    def clean(self):
        cleaned = super().clean()
        last = cleaned.get("last_inspection")
        nxt = cleaned.get("next_inspection")
        asset_code = cleaned.get("asset_code")
        site = cleaned.get("site")

        # Ensuring that the next inspection is not before last inspection
        if last and nxt and nxt < last:
            raise ValidationError({
                "next_inspection": "Next inspection must be on or after last inspection."
            })

        # Enforcing unique asset_code per site
        if asset_code and site:
            qs = ScaffoldComponent.objects.filter(asset_code=asset_code, site=site)
            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise ValidationError({
                    "asset_code": "An asset with this code already exists for this site."
                })

        return cleaned

    def clean_last_inspection(self):
        date = self.cleaned_data.get("last_inspection")
        if date is None:
            raise ValidationError("Invalid date — please use YYYY-MM-DD format.")
        return date

    def clean_next_inspection(self):
        date = self.cleaned_data.get("next_inspection")
        if date is None:
            raise ValidationError("Invalid date — please use YYYY-MM-DD format.")
        return date
