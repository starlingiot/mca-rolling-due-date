# from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, reverse
from django.views.generic import ListView, DetailView, View

from mca_test_monitor.orders.forms import SheetUploadForm
from mca_test_monitor.orders.models import Order, TestType, Note
from mca_test_monitor.orders.utils import sheet_to_orders


class RollingDueDateView(ListView):
    model = Order

    template_name = "orders/rdd.html"

    def get_queryset(self):
        qs = super().get_queryset()
        return (
            qs.filter(tests__executed_date__isnull=True)
            .distinct()
            .prefetch_related("tests", "notes")
            .select_related("sample", "client")
            .order_by("due_date", "-created")
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        object_list = object_list or self.get_queryset()
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["upload_form"] = SheetUploadForm()
        context["colors"] = {
            tt.short_name: tt.default_color for tt in TestType.objects.all()
        }

        custom_keys = ["upload_form", "note_form"]
        for key in custom_keys:
            if kwargs.get(key):
                context[key] = kwargs.get(key)

        return context

    def post(self, request, *args, **kwargs):
        form = SheetUploadForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            sheet_to_orders(instance)
            return redirect(reverse("orders:rolling-due-date"))
        else:
            context = self.get_context_data(upload_form=form)
            return render(
                request=request, template_name=self.template_name, context=context
            )


class OrderDetailView(DetailView):
    model = Order

    template_name = "orders/order_detail.html"


class NoteView(View):
    def post(self, request, *args, **kwargs):
        note_id = request.POST.get("noteId")
        lab_id = request.POST.get("labId")
        text = request.POST.get("text", "")

        try:
            order = Order.objects.get(lab_id__icontains=lab_id)

            if note_id:
                note = Note.objects.get(id=note_id)
            else:
                note = Note.objects.create(order=order)
            note.text = text
            note.save()
            messages.add_message(request, messages.SUCCESS, "Note saved.")
        except ObjectDoesNotExist:
            messages.add_message(
                request, messages.ERROR, "Something went wrong saving your note."
            )

        return redirect(reverse("orders:rolling-due-date"))
