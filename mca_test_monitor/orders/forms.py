from django import forms

from mca_test_monitor.orders.models import ReportFile, Note


class SheetUploadForm(forms.ModelForm):

    class Meta:
        model = ReportFile

        fields = ["document"]
