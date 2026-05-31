from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count, Sum
from django.shortcuts import redirect, render

from .importer import import_materials_from_excel
from .models import MaterialItem


def material_list(request):
    query = request.GET.get("q", "").strip()
    material = request.GET.get("material", "").strip()
    thickness = request.GET.get("thickness", "").strip()
    group = request.GET.get("group") == "1"

    items = MaterialItem.objects.all()
    if query:
        items = items.filter(
            key__icontains=query
        ) | items.filter(
            maker__icontains=query
        ) | items.filter(
            material__icontains=query
        ) | items.filter(
            place__icontains=query
        ) | items.filter(
            address__icontains=query
        )
    if material:
        items = items.filter(material=material)
    if thickness:
        items = items.filter(thickness=thickness)

    totals = items.aggregate(total_quantity=Sum("quantity"), total_weight=Sum("weight"))
    materials = MaterialItem.objects.order_by("material").values_list("material", flat=True).distinct()
    thicknesses = MaterialItem.objects.order_by("thickness").values_list("thickness", flat=True).distinct()

    if group:
        grouped_items = (
            items.values("maker", "material", "thickness", "width", "length", "place")
            .annotate(quantity=Sum("quantity"), weight=Sum("weight"), rows=Count("id"))
            .order_by("material", "thickness", "width", "length", "place")
        )
        paginator = Paginator(grouped_items, 50)
    else:
        paginator = Paginator(items, 50)

    page = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "inventory/material_list.html",
        {
            "page": page,
            "query": query,
            "selected_material": material,
            "selected_thickness": thickness,
            "materials": materials,
            "thicknesses": thicknesses,
            "group": group,
            "total_quantity": totals["total_quantity"] or 0,
            "total_weight": totals["total_weight"] or 0,
        },
    )


def import_excel(request):
    if request.method == "POST":
        excel_file = request.FILES.get("excel_file")
        if not excel_file:
            messages.error(request, "Excelファイルを選択してください。")
            return redirect("inventory:import_excel")
        if not excel_file.name.lower().endswith((".xlsx", ".xlsm")):
            messages.error(request, ".xlsx または .xlsm ファイルをアップロードしてください。")
            return redirect("inventory:import_excel")

        replace_data = request.POST.get("replace_data") == "1"
        if replace_data:
            MaterialItem.objects.all().delete()

        created, errors = import_materials_from_excel(excel_file)
        if created:
            action = "入れ替えました" if replace_data else "取り込みました"
            messages.success(request, f"SQLiteデータベースへ{created}件の材料データを{action}。")
        for error in errors[:10]:
            messages.warning(request, error)
        if len(errors) > 10:
            messages.warning(request, f"ほかに{len(errors) - 10}件のエラーがあります。")
        return redirect("inventory:material_list")

    return render(request, "inventory/import_excel.html")
