from django.core.urlresolvers import reverse
from djtables import Table, Column
from parliament.apps.alerts.models import ParliamentAlert
from rapidsms.models import Contact

def _edit_link(cell):
    if cell.row.lastSent == None:
        return reverse("alert_edit",args=[cell.row.pk])

def _send_link(cell):
    return reverse("alert_send",args=[cell.row.pk])

class AlertTable(Table):
    text = Column(value = lambda c: c.row, link = _edit_link)
    date = Column(value = lambda c: c.row.create_date,name="Create date")
    lang = Column(value = lambda c: c.row.language)
    important = Column(value = lambda c: c.row.is_important)
    send = Column(link = _send_link,value = lambda c: "Send")
    lastSent = Column(value = lambda c: c.row.sent_date,name="Last sent")

    class Meta:
        order_by = "-sent_date"
        per_page = 50

class SendAttemptsTable(Table):
    name = Column(value = lambda c: c.row.contact.name)
    date = Column(value = lambda c: c.row.date)
    status = Column(value = lambda c: "Success" if(c.row.success) else "Failure")
