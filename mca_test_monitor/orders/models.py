from django.conf import settings
from django.db import models


class TimeStampedModel(models.Model):

    created = models.DateTimeField(auto_now_add=True)

    modified = models.DateTimeField(auto_now=True)

    class Meta:

        abstract = True


class ReportFile(TimeStampedModel):

    document = models.FileField(upload_to="exports/")


class Order(TimeStampedModel):

    lab_id = models.CharField(max_length=32, unique=True, blank=True)

    matrice = models.CharField(max_length=32, blank=True, default="")

    due_date = models.DateTimeField(blank=True, null=True)

    reported_date = models.DateTimeField(blank=True, null=True)

    due = models.CharField(max_length=255, blank=True, default="")

    executed = models.CharField(max_length=255, blank=True, default="")

    three_day_tat_date = models.DateTimeField(blank=True, null=True)

    coa_url = models.URLField(blank=True, default="")

    rush_job = models.BooleanField(default=False)

    from_combo = models.BooleanField(default=False)

    sample = models.ForeignKey(
        "Sample", blank=True, null=True, on_delete=models.SET_NULL
    )

    client = models.ForeignKey(
        "Client", blank=True, null=True, on_delete=models.SET_NULL
    )

    test_types = models.ManyToManyField("TestType", blank=True, through="SampleTest")

    source = models.ForeignKey(
        "ReportFile", blank=True, null=True, on_delete=models.SET_NULL
    )

    @property
    def can(self) -> bool:
        """check for potency test"""
        return self.test_types.filter(short_name__iexact="CAN").exists()

    @property
    def mic(self) -> bool:
        """check for potency test"""
        return self.test_types.filter(short_name__iexact="MIC").exists()

    @property
    def myc(self) -> bool:
        """check for potency test"""
        return self.test_types.filter(short_name__iexact="MYC").exists()

    @property
    def wa(self) -> bool:
        """check for potency test"""
        return self.test_types.filter(short_name__iexact="WA").exists()

    @property
    def ter(self) -> bool:
        """check for potency test"""
        return self.test_types.filter(short_name__iexact="TER").exists()

    @property
    def res(self) -> bool:
        """check for potency test"""
        return self.test_types.filter(short_name__iexact="RES").exists()

    @property
    def pet(self) -> bool:
        """check for potency test"""
        return self.test_types.filter(short_name__iexact="PES").exists()

    @property
    def met(self) -> bool:
        """check for potency test"""
        return self.test_types.filter(short_name__iexact="MET").exists()


class Sample(TimeStampedModel):

    name = models.CharField(max_length=255, blank=True)


class TestType(TimeStampedModel):

    short_name = models.CharField(max_length=32, blank=True)

    long_name = models.CharField(max_length=32, blank=True)

    # used for parsing executed and due columns from Excel sheet
    sheet_key = models.CharField(max_length=32, blank=True)

    # hex color like FF22AA
    default_color = models.CharField(max_length=6, blank=True)

    # 0 = leftmost on a spreadsheet
    position = models.IntegerField(null=True)

    class Meta:
        ordering = ("position", )


class SampleTest(TimeStampedModel):

    test_type = models.ForeignKey(
        "TestType", blank=True, null=True, on_delete=models.SET_NULL
    )

    order = models.ForeignKey(
        "Order", blank=True, null=True, on_delete=models.SET_NULL, related_name="tests"
    )

    executed_date = models.DateTimeField(blank=True, null=True)


class ComboTest(TimeStampedModel):

    name = models.CharField(max_length=255, blank=True)

    tests = models.ManyToManyField("TestType", blank=True, related_name="combos")


class Client(TimeStampedModel):

    name = models.CharField(max_length=255, blank=True)


class Note(TimeStampedModel):

    text = models.TextField(blank=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL
    )

    order = models.ForeignKey(
        "Order", blank=True, null=True, on_delete=models.SET_NULL, related_name="notes"
    )
