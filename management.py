import datetime
import platform
import os

import discord
from discord.ext.commands import Bot
from steem import Steem
from steem.post import Post


client = Bot(description="Placeholder", command_prefix="!", pm_help=True)
s = Steem()

channels_list = ['389762510779187200',  # introduceyourself
                 '389608804972756993',  # steemit
                 '389762038408282112',  # bitcoin
                 '389762302330535946',  # cryptocurrency
                 '389762891823316992',  # blog
                 '389761959014432778',  # steem
                 '389764215537270787',  # crypto
                 '389764282700660737',  # health
                 '389764314313129984',  # science
                 '389890366427627520',  # technology
                 '389890644551794688',  # programming
                 '389890578499764226',  # tutorials
                 '389764366456586240'  # all_other,
                 '390791633320411137', # statistics
                 ]

tag_list = ['introduceyourself',
            'steemit',
            'bitcoin',
            'cryptocurrency',
            'blog',
            'steem',
            'crypto',
            'health',
            'science',
            'technology',
            'programming',
            'tutorials']

allowed_channels = ['387030201961545728',
                    # '390791633320411137', # community-review
                    ]

moderating_roles = ['moderators',  # Keep them lower case.
                    'developers']

bot_role = 'steemit-moderator'  # Set your bot's role here.


@client.event
async def on_ready():
    print(
        'Logged in as ' + client.user.name + ' (ID:' + client.user.id + ') | Connected to ' + str(
            len(client.servers)) + ' servers | Connected to ' + str(
            len(set(client.get_all_members()))) + ' users')
    print('--------')
    print('Current Discord.py Version: {} | Current Python Version: {}'.format(
        discord.__version__, platform.python_version()))
    print('--------')
    print('Use this link to invite {}:'.format(client.user.name))
    print('https://discordapp.com/oauth2/authorize?client_id={}&scope='
          'bot&permissions=8'.format(client.user.id))


@client.event
async def on_message(message):
    msg = message
    msgcon = msg.content
    msgaut = '@' + msg.author.name

    if bot_role not in [
        y.name.lower() for y in message.author.roles] and \
                    message.channel.id in allowed_channels:

        if message.content.startswith('https://steemit') or \
                message.content.startswith('steemit'):
            smsgcon = msgcon.split('@')[1]
            tmsgcon = msgcon.split('/')[3]
            sp = Post(smsgcon)

            if sp.time_elapsed() > datetime.timedelta(hours=2) and \
                    sp.time_elapsed() < datetime.timedelta(hours=48):
                tempmsg = await client.send_message(
                    message.channel,
                    'The post is ' + str(sp.time_elapsed())[:-7] +
                    ' hours old and earned ' + str(sp.reward))

                res = await client.wait_for_reaction(['☑'], message=msg)
                if moderating_roles[0] in [y.name.lower() for y in
                                           res.user.roles] or moderating_roles[
                    1] in [y.name.lower() for y in
                           res.user.roles]:
                    await client.delete_message(msg)
                    await client.delete_message(tempmsg)

                    if tmsgcon in tag_list:
                        dest_channel = tag_list.index(tmsgcon)
                    else:
                        dest_channel = tag_list.len()

                    await client.send_message(
                        client.get_channel(channels_list[dest_channel]),
                        content=msgaut + ' sent: ' + msgcon)

            else:
                tempmsg = await client.send_message(
                    message.channel,
                    'Your post has to be between 2h and 48h old.'
                )
                await client.delete_message(msg)

        elif message.content.startswith('!ping') and moderating_roles[0] in [
            y.name.lower() for y in message.author.roles] or moderating_roles[
            1] in [y.name.lower() for y in
                   message.author.roles]:
            await client.send_message(message.channel, ':ping_pong: Pong!')

        elif bot_role not in [y.name.lower() for y in
                              message.author.roles]:
            await client.delete_message(msg)
            await client.send_message(
                message.channel,
                content=msgaut + ' Your link has to start with '
                                 '"https://steemit" or "steemit"')


client.run(os.getenv("MANAGEMENT_BOT_TOKEN"))
