# vim: ai ts=4 sts=4 et sw=4


from rapidsms.contrib.handlers.handlers.keyword import KeywordHandler
from django.utils.translation import ugettext as _
from parliament.apps.registration.utils import en_or_ka

class ThanksHandler(KeywordHandler):
    """
    Respond to thank you requests.
    """
    en_keyword = 'thanks|thank'
    ka_keyword = 'gmad|gmahd|mahd|mad'
    keyword = '(' + en_keyword + '|' + ka_keyword + ')\.?\!?'

    def help(self):
        self.handle('')

    def handle(self, text):
        if en_or_ka(self.en_keyword, text) == 'en':
            return self.respond('You are welcome!')
        else:
            return self.respond('arafris!')
