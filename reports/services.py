import csv
import html
import io
import re
from datetime import date
from decimal import Decimal
from zipfile import ZIP_DEFLATED, ZipFile

from django.core.files.base import ContentFile
from django.db.models import Count, Sum
from django.utils import timezone

from crm.models import Client, Courier, Delivery, Order, Role, Route, User
from reports.models import Report


SUPPORTED_REPORT_FORMATS = ("html", "csv", "xlsx", "pdf", "docx")


def _today():
    return timezone.localdate()


def default_period():
    today = _today()
    return today.replace(day=1), today


def parse_period(value_from=None, value_to=None):
    fallback_from, fallback_to = default_period()
    period_from = date.fromisoformat(value_from) if value_from else fallback_from
    period_to = date.fromisoformat(value_to) if value_to else fallback_to
    if period_from > period_to:
        period_from, period_to = period_to, period_from
    return period_from, period_to


def _money(value):
    return value or Decimal("0.00")


def _choice_label(choices, value):
    return dict(choices).get(value, value or "—")


def _series(queryset, field, choices=None):
    rows = queryset.values(field).annotate(value=Count("id")).order_by(field)
    return [
        {"label": _choice_label(choices, row[field]) if choices else (row[field] or "—"), "value": row["value"]}
        for row in rows
    ]


def _dated_orders(period_from, period_to, manager=None, client_id=None, status=None):
    qs = Order.objects.select_related("client", "manager").filter(delivery_date__range=(period_from, period_to))
    if manager is not None:
        qs = qs.filter(manager=manager)
    if client_id:
        qs = qs.filter(client_id=client_id)
    if status:
        qs = qs.filter(status=status)
    return qs


def build_analytics_report(scope, period_from=None, period_to=None, user=None, client_id=None, status=None):
    period_from = period_from or default_period()[0]
    period_to = period_to or default_period()[1]
    manager = user if scope == "manager" and user and not user.roles.filter(name="Администратор системы").exists() else None
    orders = _dated_orders(period_from, period_to, manager=manager, client_id=client_id, status=status)
    deliveries = Delivery.objects.select_related("order").filter(delivery_date__range=(period_from, period_to))

    total_orders = orders.count()
    revenue = _money(orders.aggregate(total=Sum("total_amount"))["total"])
    delivered_count = deliveries.filter(status=Delivery.DeliveryStatus.DELIVERED).count()
    avg_check = revenue / total_orders if total_orders else Decimal("0.00")

    by_day = (
        orders.values("delivery_date")
        .annotate(orders=Count("id"), revenue=Sum("total_amount"))
        .order_by("delivery_date")
    )
    orders_by_day = [
        {
            "label": row["delivery_date"].isoformat() if row["delivery_date"] else "—",
            "orders": row["orders"],
            "revenue": _money(row["revenue"]),
        }
        for row in by_day
    ]

    top_clients = (
        orders.values("client__name")
        .annotate(orders=Count("id"), revenue=Sum("total_amount"))
        .order_by("-revenue", "client__name")[:10]
    )
    top_clients = [
        {"label": row["client__name"] or "—", "orders": row["orders"], "revenue": _money(row["revenue"])}
        for row in top_clients
    ]

    client_types = (
        orders.values("client__client_type")
        .annotate(orders=Count("id"), revenue=Sum("total_amount"))
        .order_by("-orders")
    )
    client_types = [
        {"label": _choice_label(Client._meta.get_field("client_type").choices, row["client__client_type"]), "orders": row["orders"], "revenue": _money(row["revenue"])}
        for row in client_types
    ]

    summary = {
        "orders": total_orders,
        "revenue": revenue,
        "avg_check": avg_check.quantize(Decimal("0.01")),
        "clients": Client.objects.count(),
        "active_clients": Client.objects.filter(status="active").count(),
        "deliveries": deliveries.count(),
        "delivered": delivered_count,
        "delivery_success_rate": round((delivered_count / deliveries.count()) * 100, 1) if deliveries.count() else 0,
    }

    if scope == "admin":
        summary.update(
            {
                "users": User.objects.count(),
                "active_users": User.objects.filter(is_active=True).count(),
                "roles": Role.objects.count(),
                "couriers": Courier.objects.count(),
                "routes": Route.objects.filter(planned_date__range=(period_from, period_to)).count(),
                "reports": Report.objects.count(),
            }
        )

    return {
        "scope": scope,
        "title": "Административная аналитика" if scope == "admin" else "Менеджерская аналитика",
        "period_from": period_from,
        "period_to": period_to,
        "summary": summary,
        "sections": {
            "orders_by_status": _series(orders, "status", Order._meta.get_field("status").choices),
            "deliveries_by_status": _series(deliveries, "status", Delivery._meta.get_field("status").choices),
            "orders_by_day": orders_by_day,
            "top_clients": top_clients,
            "client_types": client_types,
            "users_by_role": [
                {"label": row["roles__name"] or "Без роли", "value": row["value"]}
                for row in User.objects.values("roles__name").annotate(value=Count("id")).order_by("roles__name")
            ]
            if scope == "admin"
            else [],
        },
    }


def _format_decimal(value):
    if isinstance(value, Decimal):
        return f"{value:.2f}"
    return str(value)


def analytics_rows(payload):
    rows = [["Раздел", "Показатель", "Значение", "Заказы", "Выручка"]]
    for key, value in payload["summary"].items():
        rows.append(["Сводка", key, _format_decimal(value), "", ""])
    for row in payload["sections"]["orders_by_status"]:
        rows.append(["Статусы заказов", row["label"], row["value"], "", ""])
    for row in payload["sections"]["deliveries_by_status"]:
        rows.append(["Статусы доставок", row["label"], row["value"], "", ""])
    for row in payload["sections"]["orders_by_day"]:
        rows.append(["Динамика", row["label"], "", row["orders"], _format_decimal(row["revenue"])])
    for row in payload["sections"]["top_clients"]:
        rows.append(["Топ клиентов", row["label"], "", row["orders"], _format_decimal(row["revenue"])])
    for row in payload["sections"]["client_types"]:
        rows.append(["Типы клиентов", row["label"], "", row["orders"], _format_decimal(row["revenue"])])
    for row in payload["sections"].get("users_by_role", []):
        rows.append(["Пользователи по ролям", row["label"], row["value"], "", ""])
    return rows


def render_report_html(payload):
    rows = analytics_rows(payload)
    body_rows = "\n".join(
        "<tr>" + "".join(f"<td>{html.escape(str(cell))}</td>" for cell in row) + "</tr>" for row in rows[1:]
    )
    return f"""<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <title>{html.escape(payload["title"])}</title>
  <style>
    body {{ font-family: Arial, sans-serif; color: #111827; margin: 32px; }}
    h1 {{ margin-bottom: 4px; }}
    table {{ border-collapse: collapse; width: 100%; margin-top: 24px; }}
    th, td {{ border: 1px solid #d1d5db; padding: 8px 10px; text-align: left; }}
    th {{ background: #eef2ff; }}
  </style>
</head>
<body>
  <h1>{html.escape(payload["title"])}</h1>
  <div>Период: {payload["period_from"]} - {payload["period_to"]}</div>
  <table>
    <thead><tr>{''.join(f'<th>{html.escape(str(cell))}</th>' for cell in rows[0])}</tr></thead>
    <tbody>{body_rows}</tbody>
  </table>
</body>
</html>"""


def render_report_csv(payload):
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerows(analytics_rows(payload))
    return buffer.getvalue()


def _xml(value):
    return html.escape(str(value), quote=True)


def render_report_xlsx(payload):
    rows = analytics_rows(payload)
    sheet_rows = []
    for r_idx, row in enumerate(rows, start=1):
        cells = []
        for c_idx, cell in enumerate(row, start=1):
            col = chr(64 + c_idx)
            cells.append(f'<c r="{col}{r_idx}" t="inlineStr"><is><t>{_xml(cell)}</t></is></c>')
        sheet_rows.append(f'<row r="{r_idx}">{"".join(cells)}</row>')
    sheet = f'<?xml version="1.0" encoding="UTF-8"?><worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData>{"".join(sheet_rows)}</sheetData></worksheet>'
    buffer = io.BytesIO()
    with ZipFile(buffer, "w", ZIP_DEFLATED) as archive:
        archive.writestr("[Content_Types].xml", '<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/><Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/></Types>')
        archive.writestr("_rels/.rels", '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>')
        archive.writestr("xl/workbook.xml", '<?xml version="1.0" encoding="UTF-8"?><workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets><sheet name="Аналитика" sheetId="1" r:id="rId1"/></sheets></workbook>')
        archive.writestr("xl/_rels/workbook.xml.rels", '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/></Relationships>')
        archive.writestr("xl/worksheets/sheet1.xml", sheet)
    return buffer.getvalue()


def render_report_docx(payload):
    rows = analytics_rows(payload)
    paragraphs = [
        f'<w:p><w:r><w:t>{_xml(payload["title"])}</w:t></w:r></w:p>',
        f'<w:p><w:r><w:t>Период: {payload["period_from"]} - {payload["period_to"]}</w:t></w:r></w:p>',
    ]
    for row in rows:
        paragraphs.append(f'<w:p><w:r><w:t>{_xml(" | ".join(str(cell) for cell in row))}</w:t></w:r></w:p>')
    document = f'<?xml version="1.0" encoding="UTF-8"?><w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>{"".join(paragraphs)}<w:sectPr/></w:body></w:document>'
    buffer = io.BytesIO()
    with ZipFile(buffer, "w", ZIP_DEFLATED) as archive:
        archive.writestr("[Content_Types].xml", '<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/></Types>')
        archive.writestr("_rels/.rels", '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>')
        archive.writestr("word/document.xml", document)
    return buffer.getvalue()


def _pdf_escape(value):
    return re.sub(r"([\\()])", r"\\\1", str(value).encode("latin-1", "replace").decode("latin-1"))


def render_report_pdf(payload):
    lines = [payload["title"], f"Period: {payload['period_from']} - {payload['period_to']}"]
    lines.extend(" | ".join(_format_decimal(cell) for cell in row) for row in analytics_rows(payload)[1:40])
    text = " BT /F1 10 Tf 50 780 Td " + " T* ".join(f"({_pdf_escape(line)}) Tj" for line in lines) + " ET"
    objects = [
        "<< /Type /Catalog /Pages 2 0 R >>",
        "<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        "<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
        "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        f"<< /Length {len(text.encode('latin-1'))} >>\nstream\n{text}\nendstream",
    ]
    output = io.BytesIO()
    output.write(b"%PDF-1.4\n")
    offsets = [0]
    for idx, obj in enumerate(objects, start=1):
        offsets.append(output.tell())
        output.write(f"{idx} 0 obj\n{obj}\nendobj\n".encode("latin-1"))
    xref = output.tell()
    output.write(f"xref\n0 {len(objects)+1}\n0000000000 65535 f \n".encode("latin-1"))
    for offset in offsets[1:]:
        output.write(f"{offset:010d} 00000 n \n".encode("latin-1"))
    output.write(f"trailer << /Size {len(objects)+1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF".encode("latin-1"))
    return output.getvalue()


def render_report(payload, fmt):
    if fmt == "html":
        return render_report_html(payload), "text/html; charset=utf-8"
    if fmt == "csv":
        return render_report_csv(payload), "text/csv; charset=utf-8"
    if fmt == "xlsx":
        return render_report_xlsx(payload), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    if fmt == "pdf":
        return render_report_pdf(payload), "application/pdf"
    if fmt == "docx":
        return render_report_docx(payload), "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    raise ValueError(f"Unsupported report format: {fmt}")


def create_analytics_report_file(scope, fmt, period_from, period_to, user=None, client_id=None, status=None):
    fmt = fmt.lower()
    if fmt not in SUPPORTED_REPORT_FORMATS:
        raise ValueError(f"Unsupported report format: {fmt}")
    payload = build_analytics_report(scope, period_from, period_to, user=user, client_id=client_id, status=status)
    content, _ = render_report(payload, fmt)
    if isinstance(content, str):
        content = content.encode("utf-8-sig" if fmt == "csv" else "utf-8")
    stamp = timezone.now().strftime("%Y%m%d%H%M%S")
    title = f"{payload['title']} {period_from:%d.%m.%Y}-{period_to:%d.%m.%Y}"
    report = Report.objects.create(
        title=title,
        period_from=period_from,
        period_to=period_to,
        status="ready",
        validation_status="ok",
        validation_message="Отчёт сформирован автоматически.",
        created_by=user if getattr(user, "is_authenticated", False) else None,
    )
    report.file.save(f"analytics-{scope}-{stamp}.{fmt}", ContentFile(content), save=True)
    return report
