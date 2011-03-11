from rapidsms.contrib.handlers.handlers.keyword import KeywordHandler
from rapidsms.models import Connection, Backend, Contact

class ConfirmHandler(KeywordHandler):
    """Handles confirmation messages from people who have
    been added with the web interface."""
    keyword = "confirm|damowmeba|dadastureba"

    def help(self):
        self.handle("")

    def handle(self,text):
        if self.msg.connection.contact is None:
            return self.respond_error(
                "You must sign up before you can confirm!")

        if self.msg.connection.contact.is_active == True:
            return self.respond_error("You are already subscribed.")

        self.msg.connection.contact.is_active = True
        self.msg.connection.contact.save()

        return self.respond("Your subscription has been confirmed. Send LEAVE to unsubscribe.")
