from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.db.models import Q, Count, Case, When, IntegerField
from django.shortcuts import redirect, get_object_or_404
from django.views import View

from .models import ScaffoldComponent
from .forms import ScaffoldComponentForm


class AssetListView(ListView):
    model = ScaffoldComponent
    template_name = "assets/list.html"
    context_object_name = "assets"
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()

        # Filters
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

        # Custom ordering NEW → GOOD → REPAIR → SCRAP
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

        # Preserve query parameters
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


# -----------------------------------------------------------
# ✅ FINAL: Toggle is_in_use — (Assignment Requirement)
# -----------------------------------------------------------
def toggle_in_use(request, pk):
    asset = get_object_or_404(ScaffoldComponent, pk=pk)
    asset.is_in_use = not asset.is_in_use
    asset.save()
    return redirect("assets:detail", pk=pk)
