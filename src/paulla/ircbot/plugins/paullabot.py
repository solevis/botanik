import irc3
from time import sleep
from random import sample


@irc3.plugin
class PaullaBot:
    """Paullabot scenario"""
    def __init__(self, bot):
        self.bot = bot
        self.log = self.bot.log

    @irc3.event(irc3.rfc.PRIVMSG)
    def kick_this(self, mask, event, target, data):
        if mask.nick.lower() == 'paullabot':
            if "Error:" in data:
                key = data.split()[2].lower().replace('"','')
                scenar = {
                        'chut' : 'maytagueule',
                        'maytagueule' : 'Arrete de te faire du mal',
                        'arrete' : 'meme pinpin il est plus intelligent que toi!',
                        'meme' : 'Va mourir',
                        'va' : 'we need to talk ...'
                        }
                self.bot.call_with_human_delay(
                        self.bot.privmsg, target, "PaullaBot: %s" % scenar[key])
            else:
                self.bot.call_with_human_delay(
                        self.bot.privmsg, target, "PaullaBot: chut !")
                if "now ignoring you for 10 minutes." in data:
                    self.bot.send("""KICK %s PaullaBot :Error: "gnagnagna" is not a valid command.""" % target)
                    sleep(3)
                    self.bot.send("MODE %s +b PaullaBot" % target)
                    self.bot.send("""KICK %s PaullaBot :J'sais pas avec quoi t'es code, mais certainement pas avec irc3""" % target)


