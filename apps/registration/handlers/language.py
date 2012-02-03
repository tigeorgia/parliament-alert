#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4


from rapidsms.contrib.handlers.handlers.keyword import KeywordHandler
from rapidsms.models import Contact
from rapidsms.conf import settings
from django.utils.translation import ugettext as _
from apps.registration.utils import en_or_ka

class LanguageHandler(KeywordHandler):
    """
    Allow remote users to set their preferred language, by updating the
    ``language`` field of the Contact associated with their connection.
    """
    en_keyword = "language|lang"
    ka_keyword = "ena"
    keyword = en_keyword + "|" + ka_keyword

    def help(self):
        if self.msg.connection.contact == None:
            if en_or_ka(self.en_keyword,self.msg.text) == "en":
                return self.respond_error("You aren't signed up!")
            else:
                return self.respond_error("daregistrirebuli ar xart!")

        self.respond(_("To set your language, send LANGUAGE CODE. Send LANGUAGE KA for Georgian, LANGUAGE EN for English."))

    def handle(self, text):
        if self.msg.connection.contact is None:
            return self.respond_error(_("You must send JOIN before you can set your language preference."))

        t = text.lower()
        if t[-1] == '.': t = t[:-1] # remove dot as last char.

        for code, name in settings.LANGUAGES:
            if t != code.lower() and t != name.lower():
                continue

            self.msg.connection.contact.language = code
            self.msg.connection.contact.save()

            return self.respond(_("I will speak to you in English."))

        return self.respond_error(_('I only speak Georgian and English. Send LANGUAGE KA for Georgian, LANGUAGE EN for English.'))
