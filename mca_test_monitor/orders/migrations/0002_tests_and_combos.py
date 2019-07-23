"""
Load default TestTypes and ComboTests
"""
from django.db import migrations


def make_types(apps, schema_editor):
    """Create default TestTypes"""
    # CAN in LIMs file corresponds to Potency/Column D in RDD file.
    # MIC = Microbial/Col.E,
    # MYC = Mycotoxin/Col.F,
    # TER=Terpenes/Col.H,
    # RES=Solvents/Col I,
    # PES = Pesticides/Col. J,
    # MET=HMs/ColK

    test_types = [
        {"short_name": "CAN", "long_name": "Potency", "default_color": "00B050", "position": 0, "sheet_key": "cannabinoid"},
        {"short_name": "MIC", "long_name": "Microbial", "default_color": "7030A0", "position": 1, "sheet_key": "microbial"},
        {"short_name": "MYC", "long_name": "Mycotoxin", "default_color": "0070C0", "position": 2, "sheet_key": "mycotoxin"},
        {"short_name": "WA", "long_name": "Wa / Moi.", "default_color": "FFC000", "position": 3, "sheet_key": "water"},
        {"short_name": "TER", "long_name": "Terpenes", "default_color": "002060", "position": 4, "sheet_key": "terpene"},
        {"short_name": "RES", "long_name": "Solvents", "default_color": "548235", "position": 5, "sheet_key": "residual"},
        {"short_name": "PES", "long_name": "Pesticides", "default_color": "FF33CC", "position": 6, "sheet_key": "pesticide"},
        {"short_name": "MET", "long_name": "Heavy Metals", "default_color": "FA6306", "position": 7, "sheet_key": "metal"},
    ]

    TestType = apps.get_model("orders", "TestType")
    for tt in test_types:
        TestType.objects.create(**tt)


    # I-502-CO is a combination of Potency,  Mycotoxin, and Solvents.
    # So in the case of I-502-CO abbreviation, I’d need Columns D, E, and I marked.
    # For I-502-FL, we need Columns D, E, F, and G marked.

    ComboTest = apps.get_model("orders", "ComboTest")
    co = ComboTest.objects.create(name="I502CO")
    co.tests.add(TestType.objects.get(short_name="CAN"))
    co.tests.add(TestType.objects.get(short_name="MYC"))
    co.tests.add(TestType.objects.get(short_name="RES"))
    fl = ComboTest.objects.create(name="I502FL")
    fl.tests.add(TestType.objects.get(short_name="CAN"))
    fl.tests.add(TestType.objects.get(short_name="MIC"))
    fl.tests.add(TestType.objects.get(short_name="MYC"))
    fl.tests.add(TestType.objects.get(short_name="WA"))


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(make_types),
    ]
