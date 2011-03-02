from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.db import transaction
from django.shortcuts import render_to_response, get_object_or_404
from .models import Category
from .forms import CategoryForm
from .tables import CategoryTable

# Create your views here.

@transaction.commit_on_success
def categories(req, pk=None):
    category = None

    if pk is not None:
        category = get_object_or_404(
            Category, pk=pk)

    if req.method == "POST":
        if req.POST["submit"] == "Delete Category":
            category.delete()
            return HttpResponseRedirect(reverse(categories))

        else:
            category_form = CategoryForm(instance=category,data=req.POST)

            if category_form.is_valid():
                contact = category_form.save()
                return HttpResponseRedirect(
                    reverse(categories))
    else:
        category_form = CategoryForm(instance=category)

    return render_to_response(
        "categories/dashboard.html",{
            "category": category,
            "category_form": category_form,
            "category_table": CategoryTable(Category.objects.all(), request=req)
        }, context_instance=RequestContext(req))
