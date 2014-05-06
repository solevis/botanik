import logging.config
from irc3.plugins.command import command
import logging
import irc3
from irc3.utils import * 


@irc3.plugin
class Utils:
    """A plugin is a class which take the IrcBot as argument
    """

    def __init__(self, bot):
        self.bot = bot
        self.log = self.bot.log

    @command(permission='admin', public=True)
    def say(self, mask, target, args):
        """ say something on <channel>
            
            %%say <channel> <message>...
        """
        self.bot.privmsg(as_channel(args['<channel>']), ' '.join(args['<message>']))

    @command(permission='admin', public=False)
    def join(self, mask, target, args):
        """ join <channel>
            
            %%join <channel>
        """
        self.bot.join(as_channel(args['<channel>']))

    @command(permission='admin', public=True)
    def ban(self, mask, target, args):
        """ ban someone from  <channel>
            
            %%ban <nick> <channel>
        """
        self.bot.send('MODE %s +b %s' % (as_channel(args['<channel>']), args['<nick>']))

    @command(permission='admin', public=True)
    def kick(self, mask, target, args):
        """ kick someone from  <channel>
            
            %%kick <nick> [<channel>] [<reason>...]
        """
        if not args['<channel>']:
            args['<channel>'] = target
        elif args['<channel>'] and args['<reason>']:
            if not IrcString(args['<channel>']).is_channel:
                args['<reason>'].insert(0, args['<channel>'])
                args['<channel>'] = target
        if not args['<reason>']:
            self.bot.send('KICK %s %s' % (as_channel(args['<channel>']), args['<nick>']))
        else:
            self.bot.send('KICK %s %s :%s' % (as_channel(args['<channel>']), args['<nick>'], ' '.join(args['<reason>'])))

