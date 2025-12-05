import csv
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, View
from django.urls import reverse_lazy, reverse
from django.db.models import Q, Count, Case, When, IntegerField
from django.shortcuts import redirect, get_object_or_404
from .models import ScaffoldComponent
from .forms import ScaffoldComponentForm
from django.http import HttpResponse


# CRUD Views

class AssetListView(ListView):
    model = ScaffoldComponent
    template_name = "assets/list.html"
    context_object_name = "assets"
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get("q", "").strip()
        site = self.request.GET.get("site", "").strip()
        category = self.request.GET.get("category", "").strip()
        condition = self.request.GET.get("condition", "").strip()
        in_use = self.request.GET.get("in_use", "").strip()

        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(asset_code__icontains=q))
        if site:
            qs = qs.filter(site=site)
        if category:
            qs = qs.filter(category=category)
        if condition:
            qs = qs.filter(condition=condition)
        if in_use.lower() in ["true", "false"]:
            qs = qs.filter(is_in_use=(in_use.lower() == "true"))

        qs = qs.annotate(
            condition_order=Case(
                When(condition__exact="NEW", then=0),
                When(condition__exact="GOOD", then=1),
                When(condition__exact="REPAIR", then=2),
                When(condition__exact="SCRAP", then=3),
                default=4,
                output_field=IntegerField(),
            )
        ).order_by("condition_order", "name")

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["counts_by_site"] = ScaffoldComponent.objects.values("site").annotate(count=Count("id"))
        ctx["counts_by_condition"] = ScaffoldComponent.objects.values("condition").annotate(count=Count("id"))
        ctx["query_params"] = "&".join(
            ["%s=%s" % (k, v) for k, v in self.request.GET.items() if k != "page"]
        )
        ctx["SITE_CHOICES"] = ScaffoldComponent.SITE_CHOICES
        ctx["CATEGORY_CHOICES"] = ScaffoldComponent.CATEGORY_CHOICES
        ctx["CONDITION_CHOICES"] = ScaffoldComponent.CONDITION_CHOICES
        return ctx

class AssetCreateView(CreateView):
    model = ScaffoldComponent
    form_class = ScaffoldComponentForm
    template_name = "assets/form.html"
    success_url = reverse_lazy("assets:list")

class AssetDetailView(DetailView):
    model = ScaffoldComponent
    template_name = "assets/detail.html"

class AssetUpdateView(UpdateView):
    model = ScaffoldComponent
    form_class = ScaffoldComponentForm
    template_name = "assets/form.html"
    success_url = reverse_lazy("assets:list")

class AssetDeleteView(DeleteView):
    model = ScaffoldComponent
    template_name = "assets/confirm_delete.html"
    success_url = reverse_lazy("assets:list")


# Toggle is_in_use feature

def toggle_in_use(request, pk):
    asset = get_object_or_404(ScaffoldComponent, pk=pk)
    asset.is_in_use = not asset.is_in_use
    asset.save()
    return redirect("assets:detail", pk=pk)


# CSV Export Feature

class ExportCSVView(View):
    def get(self, request):
        assets = ScaffoldComponent.objects.all()
        # Apply same filters as list
        q = request.GET.get("q", "").strip()
        site = request.GET.get("site", "").strip()
        category = request.GET.get("category", "").strip()
        condition = request.GET.get("condition", "").strip()
        in_use = request.GET.get("in_use", "").strip()

        if q:
            assets = assets.filter(Q(name__icontains=q) | Q(asset_code__icontains=q))
        if site:
            assets = assets.filter(site=site)
        if category:
            assets = assets.filter(category=category)
        if condition:
            assets = assets.filter(condition=condition)
        if in_use.lower() in ["true", "false"]:
            assets = assets.filter(is_in_use=(in_use.lower() == "true"))

        # Prepare CSV response
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="scaffold_assets.csv"'

        writer = csv.writer(response)
        writer.writerow([
            "Asset Code", "Name", "Category", "Length (mm)", "Weight (kg)",
            "Condition", "Site", "Location", "Last Inspection", "Next Inspection", "In Use"
        ])
        for asset in assets:
            writer.writerow([
                asset.asset_code,
                asset.name,
                asset.category,
                asset.length_mm or "",
                asset.weight_kg,
                asset.condition,
                asset.site,
                asset.location,
                asset.last_inspection,
                asset.next_inspection,
                "Yes" if asset.is_in_use else "No",
            ])

        return response
