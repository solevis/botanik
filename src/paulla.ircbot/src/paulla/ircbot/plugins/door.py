import irc3
from irc3.plugins.cron import cron
import requests
from datetime import datetime


@irc3.plugin
class Door:
    """
    Door state plugin
    """

    def __init__(self, bot):
        self.bot = bot
        self.log = self.bot.log

    @irc3.event(irc3.rfc.PRIVMSG)
    def question(self, mask, event, target, data):
        states = ['ouvert', 'ferm',"quelqu'un"]
        places = ['lab','fablab','local']
        for state in states:
            for place in places:
                if state in data and place in data.lower():
                    r = requests.get('http://localhost:2222').json()
                    if "0" in r['state']:
                        self.bot.privmsg(target, 'Le lab est ouvert')
                    elif "1" in r['state']:
                        self.bot.privmsg(target, "Le lab est fermé")
                    break

    @cron('*/1 * * * *')
    def anoncement(self):
        r = requests.get('http://localhost:2222').json()
        last_change = datetime.strptime(r['lastchange'], "%d/%m/%Y %H:%M:%S")
        if (datetime.now() - last_change).seconds <= 60:
            for chan in self.bot.channels:
                if "0" in r['state']:
                    self.bot.privmsg(chan,'Le lab est ouvert')
                elif "1" in r['state']:
                    self.bot.privmsg(chan,'Le lab vient de fermer')
        
