#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

from rapidsms.contrib.handlers.handlers.keyword import KeywordHandler
from rapidsms.models import Contact, Connection, Backend
from django.utils.translation import ugettext as _
from parliament.apps.registration.utils import en_or_ka
from parliament.apps.categories.models import Category

# A multilingual version of registration, plus signing up for categories
class RegisterHandler(KeywordHandler):
    """
    Allow remote users to register themselves, by creating a Contact
    object and associating it with their Connection. For example::

        >>> RegisterHandler.test('join Adam Mckaig')
        ['Thank you for registering, Adam Mckaig!']

        >>> Contact.objects.filter(name="Adam Mckaig")
        [<Contact: Adam Mckaig>]

    Note that the ``name`` field of the Contact model is not constrained
    to be unique, so this handler does not reject duplicate names. If
    you wish to enforce unique usernames or aliases, you must extend
    Contact, disable this handler, and write your own.
    """
    #keyword = "register|reg|join|subscribe|gamoicere|daregistrirdi|shemogviertdi|tvalkuriadevne"
    en_keyword = "register|reg|join|subscribe"
    ka_keyword = "gamoicere|daregistrirdi|shemogviertdi|tvalkuriadevne"
    keyword = en_keyword + "|" + ka_keyword

    def help(self):
        if en_or_ka(self.en_keyword,self.msg.text) == "en":
            self.respond("To sign up, send JOIN <COMMITTEE>, e.g. JOIN ECONOMY. To subscribe to all committees, send JOIN ALL.")
        else:
            self.respond("imistvis rom daregistrirdet, gaagzavnet GAMOICERE KOMITETI, magalitad GAMOICERE EKONOMIKA. imisatvis rom sheurtde yvela komitets, gaagzavne GAMOICERE YVELAS")

    def handle(self, text):
        if self.msg.connection.contact == None: # Generate contact if first signup
            contact = Contact.objects.create(name=str(self.msg.connection.identity))
            contact.language = en_or_ka(self.en_keyword,self.msg.text)
            self.msg.connection.contact = contact
            self.msg.connection.save()

        contact = self.msg.connection.contact
        cats = Category.objects.all()
        matched_cats = []
        keywords = text.split(' ')

        for key in keywords:
            if key.upper() == 'ALL' or key.upper() == 'YVELAS' or key.upper() == 'YVELA':
                matched_cats = list(Category.objects.all())
                break
            #compare key to Category match strings.
            for cat in cats: # Probably should have implemented keywords as OneToOne field. Oops.
                # If match, add to category ids, remove from queryset
                if cat.matchesKeyword(key):
                    matched_cats.append(cat)
                    cats = cats.exclude(id=cat.id)
        
        if len(matched_cats) == 0:
            cats = Category.objects.all().order_by('?')[:2]
            examples = ""
            if contact.language == "en": # For this reason, Georgian keywords must always be last.
                                        # Sorry, that sucks, I know.
                index = 0
            else:
                index = -1
            for c in cats:
                examples = examples + " " + c.keyword_array()[index]

            return self.respond_error(_("We couldn't find any of the committees you entered. Here are some examples to get you started:")+examples)
        
        contact.categories.add(*matched_cats)
        contact.save()

        self.respond(_("Thank you for registering! To stop receiving updates, send LEAVE COMMITTEE, for example LEAVE ECONOMY or LEAVE ALL."))
