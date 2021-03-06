"""
MIT License
Copyright (c) 2020 WebKide [d.id @323578534763298816]
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import discord, random
from discord.ext import commands


class OnMessage(commands.Cog):
    """ (∩｀-´)⊃━☆ﾟ.*･｡ﾟ non-commands, bot responds to text in message """
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        pass

    @commands.Cog.listener('on_message')
    # +------------------------------------------------------------+
    # |               RESPONDS TO TEXT IN MESSAGE                  |
    # +------------------------------------------------------------+
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        if message.content.startswith('I am'):
            hello = random.choice(['Hello ', 'Hi there ', 'Howdy '])
            iam = 'I am **Moderator** 🅑🅞🅣, pleased to meet you.'
            msg = message.content[4:]
            await message.channel.send((f'{hello}' + f'*{msg}*' + f', {iam}')

def setup(bot):
    bot.add_cog(OnMessage(bot))
