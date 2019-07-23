from itertools import chain
from typing import List

import dateparser as dp
from django.utils import timezone

from mca_test_monitor.orders.models import (
    Order,
    ReportFile,
    Sample,
    TestType,
    SampleTest,
    ComboTest,
    Client,
)


class Row:
    def __init__(self, sheet_row: dict):
        self.lab_id = sheet_row.get("Laboratory ID") or ""
        self.matrice = sheet_row.get("Matrice") or ""
        self.due_date = sheet_row.get("Due Date")
        self.reported_date = sheet_row.get("Reported")
        self.due = sheet_row.get("Due") or ""
        self.executed = sheet_row.get("executed") or ""
        self.coa_url = sheet_row.get("COA") or ""

        self.sample_name = sheet_row.get("Sample Name") or ""

        self.test_type = sheet_row.get("Test Type") or ""

        self.client_name = sheet_row.get("Client") or ""

        self.combo_flag = False

    @staticmethod
    def _split_combined_tests(combined_types: str) -> List[str]:
        """break up the single string of test type names into discrete names"""
        return combined_types.strip().split(",")

    @staticmethod
    def _sanitize(input_str: str) -> str:
        """return a string, stripped and uppercased, only digits and letters"""
        return input_str.strip().upper()

    @staticmethod
    def _split_executed_string(combined_exec:str) -> List[str]:
        """break up the executed and due strings into discrete sheet_keys"""
        return combined_exec.strip().split()

    @staticmethod
    def set_executed_date(sheet_key: str, order: Order):
        """get a SampleTest by Order and sheet_key, and set it complete"""
        st = SampleTest.objects.get(sheet_key__iexact=sheet_key, order=order)
        st.executed_date = timezone.now()
        st.save()

    def set_executed_dates(self, order: Order) -> None:
        """parse a Row's executed string and """
        sheet_keys = self._split_executed_string(self.executed)
        for k in sheet_keys:
            self.set_executed_date(k, order)

    def is_combo(self, test_str: str) -> bool:
        """determine if a test type string indicated a ComboTest"""
        is_c = ComboTest.objects.filter(name__iexact=test_str).exists()
        if is_c:
            self.combo_flag = True
        return is_c

    def to_sample(self) -> Sample:
        """Get the Sample (or create it) with the name found in the Row"""
        strp = self.sample_name.strip()
        sample, _c = Sample.objects.get_or_create(
            name__iexact=strp, defaults={"name": strp}
        )
        return sample

    def to_client(self) -> Sample:
        """Get the Client (or create it) with the name found in the Row"""
        strp = self.client_name.strip()
        client, _c = Client.objects.get_or_create(name=strp, defaults={"name": strp})
        return client

    def resolve_type_str(self, test_str: str) -> List[TestType]:
        """Convert a string to a list of TestTypes, including unpacking any
        ComboTest objects"""
        sanitized = "".join([c for c in self._sanitize(test_str) if c.isalnum()])
        if self.is_combo(sanitized):
            test_types = ComboTest.objects.get(name__iexact=sanitized).tests.all()
            return list(test_types)
        else:
            tt, _c = TestType.objects.get_or_create(
                short_name__iexact=sanitized, defaults={"short_name": sanitized}
            )
            return [tt]

    def to_test_types(self) -> List[TestType]:
        """Get the required TestTypes from the Row"""
        test_shortnames = self._split_combined_tests(self.test_type)
        test_types = chain(*[self.resolve_type_str(sn) for sn in test_shortnames])
        return list(test_types)

    def to_order(self, source: ReportFile = None) -> Order:
        """Convert a Row to a fully qualified Order (w/ supporting models)"""
        san_id = self._sanitize(self.lab_id)
        order, created = Order.objects.get_or_create(
            lab_id__iexact=san_id, defaults={"lab_id": san_id}
        )

        if created:
            for tt in self.to_test_types():
                SampleTest.objects.create(test_type=tt, order=order)
            order.from_combo = self.combo_flag

        order.matrice = self.matrice
        if self.due_date:
            order.due_date = dp.parse(self.due_date)
        if self.reported_date:
            order.reported_date = dp.parse(self.reported_date)
            # full panel is reported - no need to put on the due-date list
            for st in order.tests.all():
                st.executed_date = timezone.now()
                st.save()
        else:
            self.set_executed_dates(order)

        order.due = self.due
        order.executed = self.executed
        order.coa_url = self.coa_url

        order.sample = self.to_sample()
        order.client = self.to_client()

        order.source = source or order.source

        order.save()

        return order
