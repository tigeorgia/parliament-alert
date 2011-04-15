#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

from rapidsms.contrib.handlers.handlers.keyword import KeywordHandler
from rapidsms.models import Connection, Backend, Contact
from django.utils.translation import ugettext as _
from parliament.apps.registration.utils import en_or_ka
from parliament.apps.categories.models import Category

# The inverse of Register; allows users to leave a list, or leave everything.
class RemoveHandler(KeywordHandler):
    en_keyword = "leave|unsubscribe|remove|quit"
    ka_keyword = "gamosvla|sheckveta|washla|amowera|tsashla|datovet"
    keyword = en_keyword + "|" + ka_keyword

    def help(self):
        if self.msg.connection.contact == None:
            if en_or_ka(self.en_keyword,self.msg.text) == "en":
                return self.respond_error("You aren't signed up!")
            else:
                return self.respond_error("daregistrirebuli ar xart!")

        self.respond(_("To delete your subscription, send LEAVE COMMITTEE, for example LEAVE ECONOMY, or LEAVE ALL."))
        #self.msg.connection.contact.delete()

    def handle(self,text):
        if self.msg.connection.contact == None:
            if en_or_ka(self.en_keyword,self.msg.text) == "en":
                return self.respond_error("You aren't signed up!")
            else:
                return self.respond_error("daregistrirebuli ar xart!")
        else:
            contact = self.msg.connection.contact

        cats = Category.objects.all()
        matched_cats = []
        keywords = text.split(' ')
        for key in keywords:
            if key.upper() == 'ALL' or key.upper() == 'YVELA' or key.upper() == 'YVELAS': 
                self.respond(_("You have been removed from our lists."))
                self.msg.connection.contact.delete()
                return
#compare key to Category match strings.
            for cat in cats:
# If match, add to category ids, remove from queryset
                if cat.matchesKeyword(key):
                    matched_cats.append(cat)
                    cats = cats.exclude(id=cat.id)

        if len(matched_cats) == 0:
            cats = Category.objects.all().order_by('?')[:2]
            examples = ""
            if en_or_ka(self.en_keyword,self.msg.text) == "en": # Georgian keywords must always be last.
                                                                # Sorry, that sucks, I know.
                index = 0
            else:
                index = -1
            for c in cats:
                examples = examples + " " + c.keyword_array()[index]

            return self.respond_error(_("We couldn't find any of the committees you entered. Here are some possibilities:")+examples)
        old_len = contact.categories.all().count()
        contact.categories.remove(*matched_cats)
        if contact.categories.all().count() == 0:
            self.respond(_("You have been removed from our lists."))
            self.msg.connection.contact.delete()
            return
        else:
            self.respond(_("Successfully removed subscriptions: ")+str(old_len-contact.categories.all().count()))
            contact.save()

