#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4
# encoding=utf-8

"""
RapidSMS backend to tweet messages

@author Sebastian Henschel <sebastian@transparency.ge>
@see http://transparency.ge
@license GPL v3

This backend depends on tweepy,
http://github.com/joshthecoder/tweepy .
Install it by

$ apt-get install python-tweepy

or

$ pip install tweepy 

It is also advisable to have south installed (http://south.aeracode.org/).


1) Put the directory 'backends/' into the root.


2) Unfortunately, the default identiy field is not long enough (only 100 chars)
for a complete OAuth credential string, so we have to extend RapidSMS'
connection class.Put the directory 'extensions/' into apps/<name>/ and run

$ python manage.py schemamigration rapidsms --auto

to create an appropriate migration, followed by

$ python manage.py migrate rapidsms

to migrate the database and a field oauth to the Connection model.


3) Then you need to append 'twitter' to the list of available backends in
settings.py, like so:

INSTALLED_BACKENDS = {

 # other backends ...

 'twitter': {
  'ENGINE': 'backends.twitter', 
 }
}


4) Afterwards go to https://dev.twitter.com/apps to setup an 'application' and
get the required credentials.


5) Finally, you have to put these into the field 'oauth' when
editing the connection for your contact details in the format:

consumer_key:consumer_secret:access_token:access_secret

"""

from rapidsms.backends.base import BackendBase
from rapidsms.utils.modules import try_import
tweepy = try_import('tweepy')


class TwitterError (Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)



class TwitterBackend(BackendBase):
    def configure(self, consumer_key=False, consumer_secret=False, access_token=False, access_secret=False):
        if tweepy is None:
            raise ImportError(
                'The backends.twitter engine is not available, because tweepy is not installed.')


    def receive(self, identity, text):
        pass


    def send(self, msg):
        name = msg.connection.contact.name
        self.debug('send: get OAuth credentials for %s' % name)
        credentials = msg.connection.oauth.split(':')
        if len(credentials) < 4:
            raise TwitterError('The supplied OAuth credentials are invalid')

        consumer_key = credentials[0]
        consumer_secret = credentials[1]
        access_token = credentials[2]
        access_secret = credentials[3]

        self.debug('send: prepare OAuth')
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)
        api = tweepy.API(auth)
        try:
            self.debug('send: tweet')
            api.update_status(msg.text)
            return True
        except tweepy.error.TweepError, e:
            raise TwitterError(e)
