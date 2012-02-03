from django.core.urlresolvers import reverse
from djtables import Table, Column
from apps.categories.models import Category

def _edit_link(cell):
    return reverse(
        "category_edit",
        args=[cell.row.pk])

class CategoryTable(Table):
    name = Column(link  = _edit_link)
    keywords = Column(value = lambda c: c.row.keywords)

    class Meta:
        order_by = "name"
        per_page = 50
