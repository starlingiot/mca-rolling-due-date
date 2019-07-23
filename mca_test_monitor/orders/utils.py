from typing import List

import openpyxl as oxl

from mca_test_monitor.orders.models import ReportFile, Order
from mca_test_monitor.orders.row import Row


def get_worksheet(rf: ReportFile) -> oxl.workbook.workbook.Worksheet:
    """Get the first Worksheet in a ReportFile.document"""
    wb = oxl.load_workbook(filename=rf.document, read_only=True)
    ws = wb.worksheets[0]
    return ws


def worksheet_to_rows(ws: oxl.workbook.workbook.Worksheet):
    """Generate Rows for a Worksheet"""
    row_vals = {col[0]: col[1:] for col in zip(*ws.values)}
    # I'm sorry for this ridiculous for loop
    for i in range(len(list(enumerate(row_vals.items()))[0][1][1])):
        yield Row({r: row_vals[r][i] for r in row_vals})


def sheet_to_orders(rf: ReportFile) -> List[Order]:
    """process an Excel spreadsheet to new Orders, or update existing Orders"""
    ws = get_worksheet(rf)
    rows = worksheet_to_rows(ws)
    orders = [row.to_order(rf) for row in rows]
    return orders
