from rapidsms.apps.base import AppBase
from rapidsms.log.mixin import LoggerMixin
from rapidsms.models import Connection, Contact
from rapidsms.messages.outgoing import OutgoingMessage
from apps.alerts.models import ParliamentAlert, AlertSendAttempt
from django.shortcuts import get_object_or_404
import json

class App (AppBase, LoggerMixin):
    """ Receives outgoing messages from the WebUI, then
        sends them to all Contacts with matching categories
        language, and importance preferences. """
    def _send_message(self, contact, text):
        """Send message through connection associated with this contact"""

        if not contact.default_connection:
            return False

        message = OutgoingMessage(contact.default_connection,text)
        return message.send()

    def ajax_POST_send_alert(self, params, data):
    # Get all active contacts matching this message's
        # categories and importance
#        if(data["is_important"] == "True"):
#            recipients = Contact.objects.all()
#        else:
#            recipients = Contact.objects.filter(only_important=False)
#        
#        categories = json.loads(data["categories"])
#        recipients = recipients.filter(categories__in=categories
#        ).filter(is_active=True)

        # Deliver only to those to whom we have not delivered before
        # Not sure if this is well optimized.
# Broken down, this is recipients.exclude(id__in=[people we've sent to before])
# where [people we've sent to before] is all send attempts
# whose outcome was success and whose alert matches this alert.
# The array contains the contact ids contained in those.
        #sent_to = [[atmpt.contact for atmpt in AlertSendAttempt.objects.filter(success=True).filter(alert=data["id"])]]
        recipient = get_object_or_404(Contact, pk=data["contact_id"])
#        sent_to = AlertSendAttempt.objects.filter(success=True).filter(alert=data["id"]).distinct().values_list('contact',flat=True)
#        if(len(sent_to) > 0): # I.e. we have sent to someone before
#            recipients = recipients.exclude(id__in=sent_to)
        #Otherwise, we can send to everybody, so nothing to do.

        response = {}
        response["success"] = False
#        response["results"] = [] # ids of Contacts to whom we attempted to send a message
        prev_deliveries = AlertSendAttempt.objects.filter(success=True).filter(alert=data["id"]).filter(contact=data["contact_id"])
        if (prev_deliveries.count() == 0):
        #for recipient in recipients:
            try:
                # Many of the RapidSMS backends don't define a return
                # for their functions, so we assume "None" is success.
                if self._send_message(recipient, data[recipient.language]) is not False:
                    response["success"] = True
                    #response["success"].append((recipient.id,True))
                #else:
                #    response["results"].append((recipient.id,False))
            except Exception as e:
                #response["results"].append((recipient.id,False))
                self.info(u"Exception when sending alert"+unicode(e.args))
        # If we exit the loop without any exceptions, return successful sends
        #if len(response["results"]) > 0:
        #    response["was_sent"] = True
        return response
        #alert = ParliamentAlert.objects.get(id=data["id"])
        #alert.sent = True
        #alert.save()

