"""
Handler addmobile
"""
from rapidsms.contrib.handlers.handlers.keyword import KeywordHandler
from rapidsms.models import Connection, Backend, Contact
from rapidsms.errors import MessageSendingError
from apps.categories.models import Category
from django.utils.translation import ugettext as _
from rapidsms.messages.outgoing import OutgoingMessage


class ParamError (Exception):
    """Parameter exception class"""
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


class AddMobileHandler (KeywordHandler):
    """Allows for adding a contact other than the one that
    sent the message triggering this handler, and sends a 
    confirmation message to that user to make sure they
    want to sign up."""

    keyword = 'addmobile'
    errfmt = '%d.%s: %s'
    connections = None


    def _check_num_params (self, params):
        """Check number of parameters."""
        num = len(params)
        if num != 5:
            msg = _('Wrong number of parameters. Try')
        else:
            return True

        if num == 1: 
            example = self._example(name=params[0])
        elif num == 2:
            example = self._example(name=params[0], phone_no=params[1])
        elif num == 3:
            example = self._example(name=params[0], phone_no=params[1],
                lang=params[2])
        elif num == 4:
            example = self._example(name=params[0], phone_no=params[1],
                lang=params[2], only_important=params[3])
        else:
            example = self._example()

        raise ParamError(self.errfmt % (2, msg, example))


    def _check_name (self, params):
        """Check if given name is proper."""
        if not params[0]:
            msg = _('Wrong name')
            example = self._example(phone_no=params[1], lang=params[2],
                only_important=params[3], categories=params[4])
            raise ParamError(self.errfmt % (3, msg, example))

        return params[0]


    def _check_phone_no (self, params):
        """Check if given phone number is proper."""
        if len(params[1]) != 13:
            msg = _('Wrong length of phone number. Try')
            example = self._example(name=params[0], lang=params[2],
                only_important=params[3], categories=params[4])
            raise ParamError(self.errfmt % (4, msg, example))

        try:
            int(params[1][1:])
        except ValueError:
            msg = _('Phone number not a number. Try')
            example = self._example(name=params[0], lang=params[2],
                only_important=params[3], categories=params[4])
            raise ParamError(self.errfmt % (5, msg, example))

        # Check for duplicates
        self.connections = Connection.objects.filter(identity=params[1])
        duplicates = self.connections.filter(contact__isnull=False)
        if len(duplicates) > 0:
            msg = _('Phone number already exists.')
            if not duplicates[0].contact.is_active:
                msg += ' ' + _('Maybe you meant "confirm"?')
            msg += ' ' + _('Try')
            example = self._example(name=params[0], lang=params[2],
                only_important=params[3], categories=params[4])
            raise ParamError(self.errfmt % (6, msg, example))

        return params[1]


    def _check_lang (self, params):
        """Check if given language is proper."""
        if len(params[2]) != 2 or (params[2] != "en" and params[2] != "ka"):
            msg = _('Only ka or en allowed for language. Try')
            example = self._example(name=params[0], phone_no=params[1],
                only_important=params[3], categories=params[4])
            raise ParamError(self.errfmt % (7, msg, example))

        return params[2]
 

    def _check_only_important (self, params):
        """Check if given only_important is proper."""
        only_important = params[3].upper()
        if only_important == 'FALSE':
            return False
        elif only_important == 'TRUE':
            return True
        else:
            msg = _('Only true or false allowed for ONLYIMPORTANT. Try')
            example = self._example(name=params[0], phone_no=params[1],
                lang=params[2], categories=params[4])
            raise ParamError(self.errfmt % (8, msg, example))


    def _check_categories (self, params):
        """Check if given categories is proper."""
        keywords = params[4].lower().split(', ')
        cats = Category.objects.all()
        matched_cats = []
        for key in keywords:
            #compare key to Category match strings.
            if key.upper() == 'ALL':
                matched_cats = Category.objects.all()
                break
            for cat in cats:
            # If match, add to category ids, remove from queryset
                if cat.matchesKeyword(key):
                    matched_cats.append(cat)
                    cats = cats.exclude(id=cat.id)

        if len(matched_cats) == 0:
            msg = _('No matching categories. Try')
            example = self._example(name=params[0], phone_no=params[1],
                lang=params[2], only_important=params[3])
            raise ParamError(self.errfmt % (9, msg, example))

        return matched_cats



    def _save_contact (self, data):
        """Save contact to database"""

        # Create connection, or if this is a re-register, just use (one
        # of) the old one(s).
        old_connections = self.connections.filter(contact__isnull=True)
        if len(old_connections) > 0:
            conn = old_connections[0]
        else:
            gsm_backend = Backend.objects.get(name='gsm')
            #gsm_backend = Backend.objects.get(name='message_tester')
            conn = Connection(backend=gsm_backend, identity=data['phone_no'])

        # Create contact
        contact = Contact(name=data['name'], language=data['lang'],
            is_active=False, only_important=data['only_important'])
        contact.save()
        contact.categories = data['categories']
        contact.save()
        conn.contact = contact
        conn.save()

        return contact


    def _example (self, **kwargs):
        """Returns an example how to use addmobile"""
        if 'name' in kwargs and kwargs['name']:
            name = kwargs['name']
        else:
            name = '<NAME>'

        if 'phone_no' in kwargs and kwargs['phone_no']:
            phone_no = kwargs['phone_no']
        else:
            phone_no = '+99559nnnnnnn'

        if 'lang' in kwargs and kwargs['lang']:
            lang = kwargs['lang']
        else:
            lang = '[en|ka]'

        if 'only_important' in kwargs and kwargs['only_important']:
            only_important = kwargs['only_important']
        else:
            only_important = '[True|False]'

        if 'categories' in kwargs and kwargs['categories']:
            categories = kwargs['categories']
        else:
            categories = 'ALL'

        return "%s %s %s %s %s %s" % (
            self.keyword, name, phone_no, lang, only_important, categories)


    def help(self):
        """KeywordHandler.help"""
        msg = _('No parameters. Try')
        self.respond(self.errfmt % (1, msg, self._example()))


    # This handler will fail sneakily by returning the
    # standard "I don't understand message."
    # Revised: now it returns more expressive error messages.
    #
    # This handler should be called with machine-
    # generated messages, in general.

    # addmobile <NAME> <ID> <LANG> <ONLYIMPORTANT?> <CATEGORIES>
    def handle(self, text):
        """KeywordHandler.handle"""
        # Slice text into array by spaces
        params = text.split(' ', 4)
        # remove punctuation dot as last char
        if params[-1][-1] == '.': params[-1] = params[-1][:-1]

        # Check for proper formatting (pretty strictly)
        try:
            self._check_num_params(params)
            name = self._check_name(params)
            phone_no = self._check_phone_no(params)
            lang = self._check_lang(params)
            only_important = self._check_only_important(params)
            categories = self._check_categories(params)
        except ParamError, ex:
            return self.respond_error(ex.value)

        contact = self._save_contact({
            'name': name,
            'phone_no': phone_no,
            'lang': lang,
            'only_important': only_important,
            'categories' : categories
        })

        try:
            text = _("Please confirm that you wish to be added to the TI Georgia Parliamentary Alert Service by replying 'confirm' to this message.")
            message = OutgoingMessage(contact.default_connection, text)
            message.send()
        except MessageSendingError:
            response = _('Problems sending confirmation message.' +\
                unicode(MessageSendingError.args))
            return self.respond_error(response)
        except KeyError:
            response = _('Problems sending confirmation message.')
            return self.respond_error(response)

        return self.respond(_('Contact successfully added; confirmation sent.'))
