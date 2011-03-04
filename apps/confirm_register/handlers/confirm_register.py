from rapidsms.contrib.handlers.handlers.keyword import KeywordHandler

class ConfirmRegisterHandler(KeywordHandler)
    """Allows for adding a contact other than the one that
    sent the message triggering this handler, and sends a 
    confirmation message to that user to make sure they
    want to sign up."""

    keyword = "addmobile"

    def help(self):
        self.respond("To add a user, send ADDMOBILE <NAME> <ID> "+\
                     "<LANG> <IMPORTANTONLY?> <CATEGORIES>")

    def handle(self, text):
        pass
        #contact = Contact.objects.create(
