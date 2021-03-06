from rapidsms.contrib.handlers.handlers.keyword import KeywordHandler
from rapidsms.models import Connection, Backend, Contact
from django.utils.translation import ugettext as _

class ConfirmHandler(KeywordHandler):
    """Handles confirmation messages from people who have
    been added with the web interface."""
    en_keyword = "confirm"
    ka_keyword = "damowmeba|dadastureba|vadastureb|vadaztureb|'vadastureb'|\"vadastureb\""
    keyword = "(" + en_keyword + "|" + ka_keyword + ")\.?"

    def help(self):
        self.handle("")

    def handle(self,text):
        if self.msg.connection.contact is None:
            return self.respond_error(
                _("You must sign up before you can confirm!"))

        if self.msg.connection.contact.is_active == True:
            return self.respond_error(_("You are already subscribed."))

        self.msg.connection.contact.is_active = True
        self.msg.connection.contact.save()

        return self.respond(_("Your subscription has been confirmed. Send LEAVE ALL to unsubscribe."))
