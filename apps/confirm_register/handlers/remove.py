from rapidsms.contrib.handlers.handlers.keyword import KeywordHandler
from rapidsms.models import Connection, Backend, Contact

class RemoveHandler(KeywordHandler):
    keyword = "leave|unsubscribe|gamosvla"

    def help(self):
        return self.handle("")

    def handle(self,text):
        if self.msg.connection.contact == None:
            return self.respond_error("You aren't signed up!")

        self.respond("You have been removed from our lists.")
        self.msg.connection.contact.delete()
        self.msg.connection.delete()
