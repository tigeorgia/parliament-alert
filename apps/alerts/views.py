from datetime import *
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.db import transaction
from django.shortcuts import render_to_response, get_object_or_404
from rapidsms.models import Contact
from .models import ParliamentAlert, AlertSendAttempt
from .tables import AlertTable, SendAttemptsTable
from .forms import AlertForm, SendAlertForm
from . import utils

# Create your views here.
@transaction.commit_on_success
def alerts(req, pk=None):
    alert = None

    if pk is not None:
        alert = get_object_or_404(ParliamentAlert, pk=pk)

    if req.method == "POST":
        if req.POST["submit"] == "Delete Alert":
            alert.delete()
            return redirect(alerts)

        # Otherwise, save
        alert_form = AlertForm(instance=alert,data=req.POST)
        if alert_form.is_valid():
            alert = alert_form.save()

            return redirect(alerts)
    else:
        alert_form = AlertForm(instance=alert)

    return render_to_response(
        "alerts/dashboard.html",{
            "alert": alert,
            "alert_form": alert_form,
            "alert_table": AlertTable(ParliamentAlert.objects.all(), request=req)
        }, context_instance=RequestContext(req))

# Send an alert
@transaction.commit_on_success
def send(req, pk):
    alert = get_object_or_404(ParliamentAlert, pk=pk)

    if req.method == "POST":
        if(alert.is_important == True):
            recipients = Contact.objects.all()
        else:
            recipients = Contact.objects.filter(only_important=False)
        recipients = recipients.filter(categories__in=alert.categories.all()).filter(is_active=True)
        sent_to = AlertSendAttempt.objects.filter(success=True).filter(alert=alert.id).distinct().values_list('contact',flat=True)
        recipients = recipients.exclude(id__in=sent_to)

        succ_cnt = 0
        fail_cnt = 0
        for contact in recipients:
            try:
                response = utils.send_alert(alert,contact)
                a = AlertSendAttempt(contact=contact,alert=alert,success=response["success"])
                a.save()
                if (response["success"] == True):
                    succ_cnt += 1
                else:
                    fail_cnt += 1
                # Save attempts to db
            except:
                a = AlertSendAttempt(contact=contact,alert=alert,success=False)
                a.save()
                raise
        if succ_cnt > 0:
            alert.sent_date = datetime.now()
            alert.save()
        req.session['succ'] = succ_cnt
        req.session['fail'] = fail_cnt
        return redirect('alert_send', pk)

    else:
        send_form = SendAlertForm()
        if 'succ' in req.session:
            succ = req.session['succ']
            fail = req.session['fail']
            del req.session['succ']
            del req.session['fail']
        else:
            succ, fail = None,None
        return render_to_response(
            "alerts/send.html",{
                "alert": alert,
                "succ": succ,
                "fail": fail,
                "send_form": send_form,
                "attempts_table": SendAttemptsTable(AlertSendAttempt.objects.filter(alert=alert.id), request=req)
            }, context_instance=RequestContext(req))

