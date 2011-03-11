from rapidsms.contrib.handlers.handlers.keyword import KeywordHandler
from rapidsms.models import Connection, Backend, Contact
from apps.categories.models import Category

class AddMobileHandler(KeywordHandler):
    """Allows for adding a contact other than the one that
    sent the message triggering this handler, and sends a 
    confirmation message to that user to make sure they
    want to sign up."""

    keyword = "addmobile"

    def help(self):
        self.respond("1.Sorry, RapidSMS could not understand your message.")

    # This handler will fail sneakily by returning the
    # standard "I don't understand message."
    # This is because we don't want jokers triggering signup
    # messages to random people, so the proper format
    # shouldn't be terribly easy to figure out (although it is
    # on GitHub, so it's not super secure either).
    # This handler should be called with machine-
    # generated messages, in general.

    # addmobile <NAME> <ID> <LANG> <ONLYIMPORTANT?> <CATEGORIES>
    def handle(self, text):
        pass
        # Slice text into array by spaces
        params = text.split(' ', 4)
        # Check for proper formatting (pretty strictly)
# TODO: Better multilingual support
        if((len(params) < 5 or len(params[1]) != 8 or len(params[2]) != 2) 
           or not params[1].isdigit() or 
           (params[2] != "en" and params[2] != "ka") or 
           (params[3] != "False" and params[3] != "True")):
            return self.respond_error("2.Sorry, RapidSMS could not understand your message.")
        
        keywords = params[4].split(' ')
        cats = Category.objects.all()
        matched_cats = []
        for key in keywords:
            #compare key to Category match strings.
            for cat in cats:
            # If match, add to category ids, remove from queryset
                if cat.matchesKeyword(key):
                    matched_cats.append(cat)
                    cats = cats.exclude(id=cat.id)
        if len(matched_cats) == 0:
            return self.respond_error("3.Sorry, RapidSMS could not understand your message.")

        # Obviously, the GSM backend must be enabled for this to work
        # but since it's not at the moment, we'll use bucket.
        #gsm_backend = Backend.objects.get(name='gsm')
        gsm_backend = Backend.objects.get(name='message_tester')
        # Check for duplicates
        connection_set = Connection.objects.filter(identity=params[1])
        duplicates = connection_set.filter(contact__isnull=False)
        if(len(duplicates) > 0):
            return self.respond_error("4.Sorry, RapidSMS could not understand your message.")
        # Create connection, or if this is a re-register, just use (one of) the old one(s).
        old_connections = connection_set.filter(contact__isnull=True)
        if(len(old_connections) > 0):
            conn = old_connections[0]
        else:
            conn = Connection(backend=gsm_backend,identity=params[1])
        # Create contact
        contact = Contact(name=params[0], language=params[2], is_active=False,
                            only_important=params[3]=='True')
        contact.save()
        contact.categories=matched_cats
        contact.save()
        conn.contact = contact
        conn.save()
        contact.save()

        try:
            contact.message("Please confirm that you wish to be added to the TI Georgia " +\
                    "Parliamentary Alert Service by replying 'confirm' to this message.")
        except MessageSendingError:
            return self.respond_error("Problems sending confirmation message.")
            
        return self.respond("Contact successfully added; confirmation sent.")
