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

import discord, asyncio, random, textwrap, traceback, unicodedata2 as unicodedata, requests, urllib.request, wikipedia
try:
    import inspect
except:
    pass

from discord.ext import commands
from bs4 import BeautifulSoup, SoupStrainer
from enum import Enum
from datetime import datetime as dt
from pytz import timezone as tz

_HEADERS = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR '
                          '2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; MS-RTC LM 8; '
                          'InfoPath.3; .NET4.0C; .NET4.0E) chromeframe/8.0.552.224',
            'Accept-Language': 'en-us'}

dev_list = [323578534763298816]

d = '“Scissors cut paper, paper covers rock, rock crushes lizard, ' \
    'lizard poisons Spock, Spock smashes scissors, scissors decapitate lizard, ' \
    'lizard eats paper, paper disproves Spock, Spock vaporizes rock and, ' \
    'as it’s always been, rock crushes scissors.”\n    ~Sheldon Cooper,\n\n' \
    'The Big Bang Theory S02E08 — “The Lizard-Spock Expansion”\n\n'


class RPSLS(Enum):
    rock = "\N{RAISED FIST} **Rock!**"
    paper = "\N{PAGE FACING UP} **Paper!**"  # \N{RAISED HAND WITH FINGERS SPLAYED}
    scissors = "\N{BLACK SCISSORS} **Scissors!**"
    lizard = "\N{LIZARD} **Lizard!**"
    spock = "\N{RAISED HAND WITH PART BETWEEN MIDDLE AND RING FINGERS} **Spock!**"


class RPSLSParser:
    def __init__(self, argument):
        argument = argument.lower()
        if argument == "rock":
            self.choice = RPSLS.rock
        elif argument == "paper":
            self.choice = RPSLS.paper
        elif argument == "scissors":
            self.choice = RPSLS.scissors
        elif argument == "lizard":
            self.choice = RPSLS.lizard
        elif argument == "spock":
            self.choice = RPSLS.spock
        else:
            return


class Misc(commands.Cog):
    """(∩｀-´)⊃━☆ﾟ.*･｡ﾟ Useful commands to make your life easier"""
    def __init__(self, bot):
        self.bot = bot
        self._last_result = None
        self.mod_color = discord.Colour(0x7289da)  # Blurple
        self.user_color = discord.Colour(0xed791d)  # Orange
        self.sessions = set()
        self.query_url = "https://en.oxforddictionaries.com/definition/"
        self.sess = requests.Session()
        self.d = '```css\n“Scissors cut paper, paper covers rock, rock crushes lizard, ' \
              'lizard poisons Spock, Spock smashes scissors, scissors decapitate lizard, ' \
              'lizard eats paper, paper disproves Spock, Spock vaporizes rock and, ' \
              'as it’s always been, rock crushes scissors.”``` ~Sheldon Cooper,\n' \
              'The Big Bang Theory S02E08 — “The Lizard-Spock Expansion”'

    async def format_mod_embed(self, ctx, user, success, method):
        """ Helper func to format an embed to prevent extra code """
        emb = discord.Embed()
        emb.set_author(name=method.title(), icon_url=user.avatar_url)
        emb.colour = (discord.Colour(0xed791d))
        emb.set_footer(text=f'User ID: {user.id}')
        if success:
            if method == 'ban':
                emb.description = f'{user} was just {method}ned.'
            else:
                emb.description = f'{user} was just {method}ed.'
        else:
            emb.description = f"You do not have the permissions to {method} users."

        return emb

    # +------------------------------------------------------------+
    # |                        HACKBAN                             |
    # +------------------------------------------------------------+
    @commands.command(description='Ban using ID if they are no longer in server', no_pm=True)
    async def hackban(self, ctx, userid, *, reason=None):
        """ Ban someone using ID """
        if ctx.author.id not in dev_list:
            return

        try:
            userid = int(userid)
        except:
            await ctx.send('Invalid ID!', delete_after=3)

        try:
            await ctx.guild.ban(discord.Object(userid), reason=reason)
        except:
            success = False
        else:
            success = True

        if success:
            async for entry in ctx.guild.audit_logs(limit=1, user=ctx.guild.me, action=discord.AuditLogAction.ban):
                emb = await self.format_mod_embed(ctx, entry.target, success, 'hackban')
        else:
            emb = await self.format_mod_embed(ctx, userid, success, 'hackban')
        try:
            return await ctx.send(embed=emb)
        except discord.HTTPException as e:
            if ctx.author.id == 323578534763298816:
                return await ctx.error(f'​`​`​`py\n{e}​`​`​`')
            else:
                pass

    # +------------------------------------------------------------+
    # |                        ADD ROLE                            |
    # +------------------------------------------------------------+
    @commands.command(no_pm=True)
    @commands.has_any_role('Admin', 'Mod', 'Journalist', 'Owner')
    async def addrole(self, ctx, member: discord.Member, *, rolename: str = None):
        """
        Add a role to someone else
        Usage:
        addrole @name Listener
        """
        if ctx.author.id not in dev_list:
            return

        if not member and rolename is None:
            return await ctx.send('To whom do I add which role? ╰(⇀ᗣ↼‶)╯')

        if rolename is not None:
            role = discord.utils.find(lambda m: rolename.lower() in m.name.lower(), ctx.message.guild.roles)
            if not role:
                return await ctx.send('That role does not exist. ╰(⇀ᗣ↼‶)╯')
            try:
                await member.add_roles(role)
                await ctx.message.delete()
                await ctx.send(f'Added: **`{role.name}`** role to *{member.display_name}*')
            except:
                await ctx.send("I don't have the perms to add that role. ╰(⇀ᗣ↼‶)╯")

        else:
            return await ctx.send('Please mention the member and role to give them. ╰(⇀ᗣ↼‶)╯')

    # +------------------------------------------------------------+
    # |                     REMOVE ROLE                            |
    # +------------------------------------------------------------+
    @commands.command(no_pm=True)
    async def removerole(self, ctx, member: discord.Member, *, rolename: str):
        """ Remove a role from someone else """
        if ctx.author.id not in dev_list:
            pass

        role = discord.utils.find(lambda m: rolename.lower() in m.name.lower(), ctx.message.guild.roles)
        if not role:
            return await ctx.send('That role does not exist. ╰(⇀ᗣ↼‶)╯')
        try:
            await member.remove_roles(role)
            await ctx.message.delete()
            await ctx.send(f'Removed: `{role.name}` role from *{member.display_name}*')
        except:
            await ctx.send("I don't have the perms to remove that role. ╰(⇀ᗣ↼‶)╯")

    # +------------------------------------------------------------+
    # |                     NAME                                   |
    # +------------------------------------------------------------+
    @commands.command(no_pm=True)
    async def name(self, ctx, text: str = None):
        """ Change Bot's name """
        if ctx.author.id not in dev_list:
            return

        if text is None:
            return await ctx.send("What's my new name going to be?")

        if text is not None:
            try:
                await ctx.bot.edit_profile(username=str(text[6:]))
                await ctx.send(f'Thanks for renaming me: {text}')
                await ctx.message.delete()
            except Exception as e:
                await ctx.send(f'Failed to change my name!\n```{e}```')
                pass

    # +------------------------------------------------------------+
    # |                       LOGO                                 |
    # +------------------------------------------------------------+
    @commands.command(no_pm=True)
    async def logo(self, ctx, link: str = None):
        """ Change Bot's avatar img """
        if ctx.author.id not in dev_list:
            return

        if link is None:
            return await ctx.send('You need to use an image URL as a link.')

        else:
            try:
                # with urllib.request.urlopen(link) as response:
                    #img = response.read()
                    #await ctx.bot.edit_profile(avatar=img)
                async with bot.session.get(link) as r:
                    img = await r.read()
                    await bot.user.edit(avatar=img)
                    return await ctx.send('New logo added successfully!')
                    
            except Exception as e:
                return await ctx.send(f'Failed to update logo image!\n```{e}```')

    # +------------------------------------------------------------+
    # |                     SAUCE                                  |
    # +------------------------------------------------------------+
    @commands.command(no_pm=True)
    async def sauce(self, ctx, *, command: str = None):
        """ Show source code for any command """
        if ctx.author.id not in dev_list:
            return

        if command is not None:
            i = str(inspect.getsource(self.bot.get_command(command).callback))

            if len(i) < 1980:
                source_full = i.replace('```', '`\u200b`\u200b`')
                await ctx.send('```py\n' + source_full + '```')

            if len(i) > 1981:
                source_trim = i.replace('```', '`\u200b`\u200b`')[:1980]
                await ctx.send('```py\n' + source_trim + '```')

        else:
            await ctx.send(f"Tell me what cmd's source code you want to see.")

    # +------------------------------------------------------------+
    # |                     CHARINFO                               |
    # +------------------------------------------------------------+
    @commands.command()
    async def charinfo(self, ctx, *, characters: str):
        """
        Return UNICODE characters
        Usage:
        charinfo ā
        """
        if len(characters) > 15:
            return await ctx.send('Too many characters ({}/15)'.format(len(characters)))

        else:
            fmt = '​`{2}​` — `\\U{0:>08}​`\n​```tex\n\\N{{{1}}}​```'

            def to_string(c):
                digit = format(ord(c), 'x')
                name = unicodedata.name(c, 'Name not found.')
                return fmt.format(digit, name, c)

            e = discord.Embed(color=self.user_color)
            e.description = '\n'.join(map(to_string, characters))
            # e.add_field(name='', value=f"```tex\n\\N{{{1}}}​```")
            await ctx.send(embed=e)

    # +------------------------------------------------------------+
    # |                       URBAN                                |
    # +------------------------------------------------------------+
    @commands.command()
    async def urban(self, ctx, *, search_terms: str = None):
        """ Urban Dictionary search """
        if search_terms is None:
            return await ctx.send('What should I search for you?')

        else:
            search_terms = search_terms.split()
            definition_number = terms = None

            try:
                definition_number = int(search_terms[-1]) - 1
                search_terms.remove(search_terms[-1])
            except ValueError:
                definition_number = 0

            if definition_number not in range(0, 11):
                pos = 0
            search_terms = "+".join(search_terms)
            url = "http://api.urbandictionary.com/v0/define?term=" + search_terms
            async with self.bot.session.get(url) as r:
                result = await r.json()
            emb = discord.Embed()
            emb.colour = (discord.Colour(0xed791d))

            if result.get('list'):
                definition = result['list'][definition_number]['definition']
                example = result['list'][definition_number]['example']
                defs = len(result['list'])
                search_terms = search_terms.split("+")
                emb.title = "{}  ({}/{})".format(" ".join(search_terms), definition_number + 1, defs)
                emb.description = definition
                emb.add_field(name='Example', value=example)

            else:
                emb.title = f"Didn't find anything for *{search_terms}*"

            try:
                await ctx.send(embed=emb)
            except Exception as e:
                tb = traceback.format_exc()
                return await ctx.send(f'```css\n[OOPS, I DID IT AGAIN]\n{e}```\n```py\nヾ(ﾟ∀ﾟ○)ﾂ三ヾ(●ﾟдﾟ)ﾉ\n\n{tb}```')

    # +------------------------------------------------------------+
    # |                          WIKIPEDIA                         |
    # +------------------------------------------------------------+
    @commands.command()
    async def wiki(self, ctx, *, search: str = None):
        """ Wikipedia search command """
        if search == None:
            await ctx.channel.send(f'Usage: `{ctx.prefix}wiki [search terms]`', delete_after=23)
            return

        results = wikipedia.search(search)
        if not len(results):
            no_results = await ctx.channel.send("Sorry, didn't find any result.", delete_after=23)
            await asyncio.sleep(5)
            await ctx.message.delete(no_results)
            return

        newSearch = results[0]
        try:
            wik = wikipedia.page(newSearch)
        except wikipedia.DisambiguationError:
            more_details = await ctx.channel.send('Please input more details.', delete_after=23)
            await asyncio.sleep(5)
            await ctx.message.delete(more_details)
            return

        emb = discord.Embed()
        emb.colour = (discord.Colour(0xed791d))
        emb.title = wik.title
        emb.url = wik.url
        textList = textwrap.wrap(wik.content, 500, break_long_words=True, replace_whitespace=False)
        emb.add_field(name="Wikipedia Results", value=textList[0] + "...")
        await ctx.send(embed=emb)

    # +------------------------------------------------------------+
    # |               Oxford English Dictionary                    |
    # +------------------------------------------------------------+
    @commands.command(name='dict', description='Oxford English Dictionary', aliases=['oed'])
    async def _dict(self, ctx, *, term: str = None):
        """ Search definitions in English """
        if term is None:  # Simple usage return for invoking an empty cmd
            sample = random.choice(['lecture', 'fantasy', 'gathering', 'gradually ', 'international', 'desire'])
            v = f'{ctx.prefix}{ctx.invoked_with} {sample}'
            usage = f'**Usage:** basic results\n{v}\n\n' \
                f'**Advanced Usage:** add any parameter\n{v} `examples` `synonyms` `proverbs` `sourcecode`'
            return await ctx.send(usage)
        await ctx.channel.trigger_typing()

        query = ''.join(term.split(' ')[0])  # We only want to search the first term, the rest is for extra result
        url = f"{self.query_url}{query.lower()}"  # we lower it so it works as part of the search link
        page = requests.get(url, headers=_HEADERS)  # requests code, use the headers to appear like a normal browser
        e = discord.Embed(color=self.user_color)  # This command is EMBED-only, it doesn't work without embed perms
        x = "https://media.discordapp.net/attachments/541059392951418880/557660549073207296/oxford_favicon.png"

        try:
            e.set_author(name=f'Definition of {query.title()} in English by Oxford Dictionaries', url=url, icon_url=x)

            # SoupStrainer is required to load 1/3 of the page, discarding unnecessary content
            # "gamb" contains definition, "etym" contains pronunciation and origin
            _section_content = SoupStrainer("section", attrs={"class": ["gramb", "etymology etym", "pronSection etym"]})

            # Then we parse the resulting web page with Beautiful Soup 4
            soup = BeautifulSoup(page.content, "html.parser", parse_only=_section_content, from_encoding="utf-8")

            # ================= Send HTML5 code as a message into chat ====================
            if ctx.message.content.endswith('sourcecode') and query is not 'sourcecode':
                # This is mostly for debugging purposes, if cmd doesn't give a result, check that the code works,
                # if `code` returns empty, it is because the command couldn't find a valid page for {query}
                defs = soup.find('section', attrs={"class": "gramb"})  # sends page parsed as HTML5
                if defs is not None:
                    block = await ctx.send(f'```html\n{defs.prettify()[:1970]}``` Chars: `{len(defs.text)}`')
                    await block.add_reaction('\N{WHITE HEAVY CHECK MARK}')

            # ============= Word and its classification and pronunciation ================
            classification = soup.find('span', attrs={"class": "pos"})  # noun, verb, adjective, adverb, etc...
            if classification is not None:
                cl = f"*`[{classification.text}]`*  " or "\u200b"
                e.title = cl  # f"{cl}{query.title()}{pr.replace('/', '')}"
            # =============================================================================
            definition = soup.find('span', attrs={"class": "ind"})  # first description
            if definition is not None:  # BUG-HUNTER, 1ˢᵗ 2ⁿᵈ 3ʳᵈ, 4ᵗʰ
                # Checks for a definition, if not found, it defaults to fail-safe description below
                e.description = f"1. {definition.text[:500]}"  # await ctx.send(first.text[:500])  # BUG-HUNTER
            # ===================== if cmd *args == 'examples' ============================
            if 'examples' in ctx.message.content and query is not 'examples':
                example_1 = soup.find('div', attrs={"class": "exg"})  # first example
                if example_1 is not None:
                    ex_1 = f'*{example_1.text[1:]}*' or "\u200b"
                    try:
                        example_2 = soup.find_all('div', attrs={"class": "exg"})[1]
                        list_1 = example_2.text[1:].replace("’ ‘", "’*\n*‘")
                        ex_2 = f'\n*{list_1}'
                    except IndexError:  # ResultSet object has no attribute '.text'
                        ex_2 = "\u200b"
                    result = f"{ex_1}{ex_2}"  # This is merely aesthetic so that it ends with ... or not
                    if result[:800].endswith("’"):  # We expect it to ed well
                        complete = f'{result[:800]}*'
                    else:  # if it doesn't, then we format it properly here
                        complete = f'{result[:800]}...*'
                    e.add_field(name='Examples', value=complete, inline=False)  # BUG-HUNTER

            # ======================= First Synonyms in result =============================
            try:
                synonyms_1 = soup.find('div', attrs={"class": "synonyms"})  # .find_all('strong')  # Synonyms for search
                if synonyms_1 is not None:
                    results = synonyms_1.text
                    syns = results.replace('Synonyms', '').replace('View synonyms', '') or "#z"
                    if 'synonyms' in ctx.message.content and query is not 'synonyms':
                        e.add_field(name='Synonyms', value=f'```bf\n{syns[:460]}```', inline=False)  # BUG-HUNTER
                    else:
                        synonyms_2 = soup.find('div', attrs={"class": "exs"})
                        res = synonyms_2.find_all('strong').text
                        e.add_field(name='Synonyms', value=f'```bf\n{res}```', inline=False)  # BUG-HUNTER
                    # await ctx.send(phrases.text[:270])  # BUG-HUNTER
            except AttributeError:  # ResultSet object has no attribute '.text'
                pass

            # ======================= Output proverbs and samples ==========================
            proverb = soup.find('div', attrs={"class": "trg"})
            if proverb is not None:
                try:
                    proverb.find('div', attrs={"span": "sense-registers"})  # Proverb, {query} used in sentences
                    x = proverb.text.replace("’ ‘", "’\n‘").replace(". ‘", ".\n\n‘")
                    if 'proverbs' in ctx.message.content and query is not 'proverbs':
                        z = '’'.join(x.split("’")[3:-4])  # split x and output after 'More example sentences...'
                        e.add_field(name='Proverb', value=f"*{z[1:][:960]}...*", inline=False)
                    else:
                        z = '’'.join(x.split("’")[3:-2])
                        e.add_field(name='Proverb', value=f"*{z[1:][:240]}...*", inline=False)
                        # return await ctx.send(z[:1600])  # BUG-HUNTER
                except TypeError:  # TypeError: unhashable type: 'slice' in [:260]
                    pass

            # =================== Word Origin ETYMOLOGY [working] =========================
            try:
                pronunciation_2 = soup.find('span', attrs={"class": "phoneticspelling"})  # etymology & pronunciation
                if pronunciation_2 is not None:
                    try:
                        classification_2 = soup.find_all('section', attrs={"class": "etymology etym"})[1].find('p').text
                        msg = f'\n**Origin:** *{classification_2}*'
                    except IndexError:  # ResultSet object has no attribute '.text'
                        msg = ""
                    pro = f"**Pronunciation:** `({pronunciation_2.text})`" or "N/A"
                    e.add_field(name=f'Etymology of {query.title()}', value=f"{pro.replace('/', '')}{msg[:750]}",
                                inline=False)
                    # await ctx.send(msg[:750])  # BUG-HUNTER
            except IndexError:  # ResultSet object has no attribute '.text'
                pass
            # ================== copyright acknowledgments ================================
            e.set_footer(text=f'Oxford University Press © 2018 | Duration: {self.bot.ws.latency * 1000:.2f} ms')
            # ================== Fail-safe for words without a definition =================
            if not definition:
                e.description = f"Whoopsie! I couldn't find a definition for *{query}*.\n" \
                    f"Check spelling, or look for a variation of {query} as verb, noun, etc."

            try:
                return await ctx.send(embed=e)
            except Exception as e:
                tb = traceback.format_exc()
                return await ctx.send(f'```css\n[DAFUQ]\n{e}```\n```py\n、ヽ｀、ヽ｀个o(･･｡)｀ヽ、｀ヽ、\n\n{tb}```')

            # await ctx.message.add_reaction('thankful:389969145019498502')
        except Exception as e:
            tb = traceback.format_exc()
            return await ctx.send(f'```css\n[OOPS, I DID IT AGAIN]\n{e}```\n```py\nヾ(ﾟ∀ﾟ○)ﾂ三ヾ(●ﾟдﾟ)ﾉ\n\n{tb}```')

    # +------------------------------------------------------------+
    # |                          SAY                               |
    # +------------------------------------------------------------+
    @commands.command(no_pm=True)
    async def say(self, ctx, *, msg=''):
        """ Bot sends message """
        if f'{ctx.prefix}{ctx.invoked_with}' in msg:
            return await ctx.send("Don't ya dare spam. ( ᗒᗣᗕ)", delete_after=23)

        if not msg:
            return await ctx.send('Nice try. (｡◝‿◜｡)', delete_after=23)

        else:
            msg = ctx.message.content
            said = ' '.join(msg.split("say ")[1:])
            await ctx.send(said)  # Now it works!

    # +------------------------------------------------------------+
    # |                     SAY DELET                              |
    # +------------------------------------------------------------+
    @commands.command(no_pm=True)
    async def sayd(self, ctx, *, msg=''):
        """ Sends message and delete original """
        if f'{ctx.prefix}{ctx.invoked_with}' in msg:
            return await ctx.send("Don't ya dare spam. ( ᗒᗣᗕ)", delete_after=23)

        if not msg:
            return await ctx.send('Nice try. (｡◝‿◜｡)')

        else:
            msg = ctx.message.content
            said = ' '.join(msg.split("sayd ")[1:])

            try:
                await ctx.message.delete()
            except discord.Forbidden:
                pass
            finally:
                return await ctx.send(said)  # Now it works!

    # +------------------------------------------------------------+
    # |                      GEN                                   |
    # +------------------------------------------------------------+
    @commands.command(aliases=['general'], no_pm=True)
    async def g(self, ctx, channel: discord.TextChannel, *, message: str = None):
        """ Send a msg to another channel """
        ma = ctx.message.author.display_name
        if not channel:
            return await ctx.send(f'To what channel should I send a message {ma}?')

        if message is None:
            return await ctx.send('To send a message to a channel, tell me which channel first')

        if message is not None:
            try:
                await channel.send(message)
                try:
                    await ctx.message.add_reaction('\N{WHITE HEAVY CHECK MARK}')
                except discord.Forbidden:
                    pass
                return await ctx.channel.send(f'Success {ma}!')

            except discord.Forbidden:
                await ctx.send(f"{ma}, I don't have permissions to message in {channel}", delete_after=23)

        else:
            pass

    # +------------------------------------------------------------+
    # |                     Word/Name-generator                    |
    # +------------------------------------------------------------+
    @commands.command(aliases=['word_ai'])
    async def wordai(self, ctx, results: int = None):
        """ Generate words artificially """
        vow = ['a', 'i', 'u', 'e', 'o', 'y', '', 'a', 'i', 'u', 'e', 'o', '']
        con = [
            'qu', 'w', 'wh', 'r', 't', 'th', 'y', 'p', 'mp', 's', 'ss', 'd', 'f', 'g', 'gü',
            'ß', 'h', 'j', 'ji', 'k', '', 'l', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ''
        ]
        word = f'{random.choice(vow)}{random.choice(con)}{random.choice(vow)}' \
               f'{random.choice(vow)}{random.choice(con)}{random.choice(vow)}' \
               f'{random.choice(con)}{random.choice(vow)}{random.choice(con)}'
        word = word.title()
        
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass
        finally:
            for int in results:
                if results is None:
                    return await ctx.send(name, delete_after=69)
                if results is not None:
                    x = random.randint(3, 9)
                    name = word[:x]
                    await ctx.sen(name)


    # +------------------------------------------------------------+
    # |              Shrink text and make it tiny                  |
    # +------------------------------------------------------------+
    @commands.command(no_pm=True)
    async def tiny(self, ctx, *, text: str = None):
        """ Convert any text into a tiny ᵗᵉˣᵗ """
        if text is None:
            return await ctx.send("You have to input some text first.", delete_after=23)

        if text.lower() is not None:
            msg = ""
            char = "abcdefghijklmnopqrstuvwxyz0123456789+-+()."
            tran = "ᵃᵇᶜᵈᵉᶠᵍʰⁱʲᵏˡᵐⁿᵒᵖ٩ʳˢᵗᵘᵛʷˣʸᶻ₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎•"
            table = str.maketrans(char, tran)
            tinify = text.translate(table)
            result = f'{msg}{tinify[::1]}'
            await ctx.send(result)
        
    # +------------------------------------------------------------+
    # |                       PURGE                                |
    # +------------------------------------------------------------+
    @commands.command(aliases=['del', 'p', 'prune'], bulk=True, no_pm=True)
    async def purge(self, ctx, limit: int):
        """ Delete a number of messages """
        if ctx.author.id not in dev_list:
            return

        else:
            try:
                if not limit:
                    return await ctx.send('Enter the number of messages you want me to delete.', delete_after=23)

                if limit < 99:
                    await ctx.message.delete()
                    deleted = await ctx.channel.purge(limit=limit)
                    succ = f'₍₍◝(°꒳°)◜₎₎ Successfully deleted {len(deleted)} message(s)'
                    await ctx.channel.send(succ, delete_after=9)

                else:
                    await ctx.send(f'Cannot delete `{limit}`, try less than 100.', delete_after=23)
                 
            except discord.Forbidden:
                pass

    # +------------------------------------------------------------+
    # |         Rock paper, scissors, lizard, Spock                |
    # +------------------------------------------------------------+
    @commands.command(description=d, aliases=['rpsls', 'rps'], no_pm=True)
    async def settle(self, ctx, your_choice: RPSLSParser = None):
        """ Play rock paper scissors lizard spock """
        await ctx.channel.trigger_typing()
        author = ctx.message.author.display_name
        mod_bot = self.bot.user.display_name
        errored = f"{self.d}\n\n**Usage:**\n{ctx.prefix}{ctx.invoked_with} [rock, paper, scissors, lizard, or spock]"

        if your_choice is None:
            return await ctx.send(errored, delete_after=69)

        elif your_choice is not None:
            try:
                player_choice = your_choice.choice
                available = RPSLS.rock, RPSLS.paper, RPSLS.scissors, RPSLS.lizard, RPSLS.spock
                bot_choice = random.choice(available)
                cond = {
                    (RPSLS.rock, RPSLS.paper): False,
                    (RPSLS.rock, RPSLS.scissors): True,
                    (RPSLS.rock, RPSLS.lizard): True,
                    (RPSLS.rock, RPSLS.spock): False,
                    (RPSLS.paper, RPSLS.rock): True,
                    (RPSLS.paper, RPSLS.scissors): False,
                    (RPSLS.paper, RPSLS.lizard): False,
                    (RPSLS.paper, RPSLS.spock): True,
                    (RPSLS.scissors, RPSLS.rock): False,
                    (RPSLS.scissors, RPSLS.paper): True,
                    (RPSLS.scissors, RPSLS.lizard): True,
                    (RPSLS.scissors, RPSLS.spock): False,
                    (RPSLS.lizard, RPSLS.rock): False,
                    (RPSLS.lizard, RPSLS.paper): True,
                    (RPSLS.lizard, RPSLS.scissors): False,
                    (RPSLS.lizard, RPSLS.spock): True,
                    (RPSLS.spock, RPSLS.rock): True,
                    (RPSLS.spock, RPSLS.paper): False,
                    (RPSLS.spock, RPSLS.scissors): True,
                    (RPSLS.spock, RPSLS.lizard): False
                }
                e = discord.Embed()
                e.add_field(name=f'{mod_bot} chose:', value=f'{bot_choice.value}', inline=True)
                e.add_field(name=f'{author} chose:', value=f'{player_choice.value}', inline=True)

                if bot_choice == player_choice:
                    outcome = None

                else:
                    outcome = cond[(player_choice, bot_choice)]

                if outcome is True:
                    e.color = (discord.Colour(0xed791d))
                    e.set_footer(text="\N{SMALL ORANGE DIAMOND} You win!")
                    await ctx.channel.send(embed=e)

                elif outcome is False:
                    e.color = (discord.Colour(0xe000ff))
                    e.set_footer(text="\N{NO ENTRY SIGN} You lose...")
                    await ctx.channel.send(embed=e)

                else:
                    e.color = (discord.Colour(0x7289da))
                    e.set_footer(text="\N{JAPANESE SYMBOL FOR BEGINNER} We're square")
                    await ctx.channel.send(embed=e)

            except AttributeError:
                return await ctx.send(errored, delete_after=369)

    # +------------------------------------------------------------+
    # |                   Pick from list                           |
    # +------------------------------------------------------------+
    @commands.command(description='Choose from a list of items', no_pm=True)
    async def choose(self, ctx, *, options: str = None):
        """ Pick an item from a list """
        msg = f'Write at least two options separated by a comma: ' \
              f'```css\n{ctx.prefix}{ctx.invoked_with} eat, sleep, read or ' \
              f'walk```'.replace('<@726650866169282600>', f'@{self.bot.user.name}')

        if options is None:
            return await ctx.send(msg, delete_after=23)

        if options is not None:
            valid_separators = [',', '|', ' or ']

            if any(x in options for x in valid_separators):
                skd = options.replace(',', ', ').replace(' or ', ', ').replace('|', ', ') \
                    .replace('.', ', ').replace('  ', ' ')
                picked = random.choice(skd.split(', '))
                x = f'```ruby\nOptions:\n{skd}```\N{SMALL ORANGE DIAMOND} I choose: **`{picked}`**'

                try:
                    e = discord.Embed(color=0xed791d)
                    e.description = x.replace(' , ', ', ')
                    await ctx.send(embed=e)

                except discord.Forbidden:  # FORBIDDEN (status code: 403): Missing Permissions
                    result = f'I choose **{picked}** for you.'
                    return await ctx.send(result)

            else:
                return await ctx.send(msg, delete_after=23)

        else:
            return await ctx.send(msg, delete_after=23)

    # +------------------------------------------------------------+
    # |     Very basic cmd to flip names or coins                  |
    # +------------------------------------------------------------+
    @commands.command(description='Settle a dispute via coin toss', aliases=['toss', 'tosacoin'], no_pm=True)
    async def flip(self, ctx, *, something: str = None):
        """Flips a coin... or some text.
        Defaults to coin toss.
        """
        h = 'https://media.discordapp.net/attachments/541059392951418880/556977776771596333/1926_heads.png'
        t = 'https://media.discordapp.net/attachments/541059392951418880/556977839166193674/1926_tails.png'
        e = 'https://media.discordapp.net/attachments/541059392951418880/556978114354348052/1926_edge.png'
        if something is not None:
            char = "abcdefghijklmnopqrstuvwxyz"
            tran = "ɐqɔpǝɟƃɥᴉɾʞʅɯuodbɹsʇnʌʍxʎz"
            table = str.maketrans(char, tran)
            name = something.translate(table)
            char = char.upper()
            tran = "∀ꓭƆᗡƎℲ⅁HIſꓘ⅂WNOԀQᴚSꓕՈΛMX⅄Z"  # ⊥∩āɐ̱
            table = str.maketrans(char, tran)
            name = name.translate(table)

            em = discord.Embed(color=self.user_color)
            em.add_field(name=f'{ctx.message.author.display_name}', value=f'(╯°□°）╯︵ **{name[:1980][::-1]}**')

            try:
                await ctx.send(embed=em)
            except discord.HTTPException:
                await ctx.send(name[:1980][::-1])

        else:
            flips = random.randint(3, 101)
            toss = f'After being tossed up,\nthe coin flipped\n{flips} times in the air\nand landed showing:'
            flop = f'*What are the odds?*\nAfter spinning {flips} times\nthe coin managed to\nland on its:'

            heads = discord.Embed(color=0xa84300, description=toss)
            heads.set_thumbnail(url=h)
            heads.add_field(name='\N{SMALL ORANGE DIAMOND} Heads', value='`1926 Golden Dollar`')

            tails = discord.Embed(color=0x1f8b4c, description=toss)
            tails.set_thumbnail(url=t)
            tails.add_field(name='\N{SMALL ORANGE DIAMOND} Tails', value='`1926 Golden Dollar`')

            edge = discord.Embed(color=0x23272a, description=flop)  # odds are 11/1
            edge.set_thumbnail(url=e)
            edge.add_field(name='\N{BLACK SMALL SQUARE} Edge', value='...try again')

            result = random.choice([heads, tails, heads, tails, heads, tails, heads, tails, heads, tails, edge])

            try:
                await ctx.send(embed=result)

            except discord.HTTPException:
                await ctx.send(random.choice(['Heads', 'Tails']))

    # +------------------------------------------------------------+
    # |                     Guess                                  |
    # +------------------------------------------------------------+
    @commands.command(no_pm=True)
    async def guess(self, ctx, number: int = None):
        """ Write number between 1 and 11 """
        answer = random.randint(1, 11)
        guessed_wrong = [
            'Not even close, the right number was:',
            'Better luck next time, the number was:',
            'How could you have known that the number was:',
            'Hmm, well, the right number was:',
            'Not getting any better, the number was:',
            'Right number was:'
        ]
        wrong = f'```{random.choice(guessed_wrong)} {answer}```'
        guessed_right = [
            'You guessed correctly!',
            'Everyone knew you could do it!',
            'You got the right answer!',
            'History will remember you...'
        ]
        right = f'```{random.choice(guessed_right)}```'
        u = ctx.message.author.display_name
        e = discord.Embed(color=self.user_color)

        if number is None:
            return await ctx.send('please choose a number between 1 and 11', delete_after=23)

        if number is not None:
            if number < answer or number > answer:
                q_mark = '\N{OCTAGONAL SIGN}'
                e.add_field(name=f'{q_mark} {u} chose: `{number}`',
                            value=wrong, inline=True)
                try:    await ctx.send(embed=e)
                except discord.HTTPException:    await ctx.send(wrong)

            if number == answer:
                q_mark = '\N{SPORTS MEDAL}'
                e.add_field(name=f'{q_mark} {u} chose: `{answer}`',
                            value=right, inline=True)
                try:    await ctx.send(embed=e)
                except discord.HTTPException:    await ctx.send(right)

            else:    pass

    # +------------------------------------------------------------+
    # |                       Clap                                 |
    # +------------------------------------------------------------+
    @commands.command()
    async def clap(self, ctx, *, msg: str = None):
        """ Clap that message! """
        if msg is not None:
            if len(msg.split(' ')) > 1:
                text = msg.replace(' ', ' :clap: ')
                await ctx.send(text)
            else:    await ctx.send(':clap:')

        else:
            try:    await ctx.send(':clap:')
            except discord.HTTPException as e:
                if ctx.author.id == 323578534763298816:
                    await ctx.send(f'​`​`​`{e}​`​`​`', delete_after=15)
                else:    pass

def setup(bot):
    bot.add_cog(Misc(bot))
