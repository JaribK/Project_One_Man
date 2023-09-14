# import main(discord)

import os
import discord
import yt_dlp as youtube_dl
import asyncio
import time
import itertools
import openai

# from

from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv
from functools import partial
from async_timeout import timeout
from googletrans import Translator
from googleapiclient.discovery import build

############################################################################################################################################

# sub import
import random
import datetime

############################################################################################################################################

# import from other_files

from randomfoods import list_of_Foods

############################################################################################################################################

# starter

load_dotenv()

token = os.getenv('TOKEN')

openai.api_key = os.getenv('OPENAI_API_KEY')

GGIMAGEPAI = os.getenv('GGIMAGEAPI')

intents = discord.Intents.default()

intents.message_content = True

bot = commands.Bot(command_prefix = "-", intents = intents , activity = discord.Game(name="-help") )

############################################################################################################################################

# class anythings

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0', # bind to ipv4 since ipv6 addresses cause issues sometimes
    'force-ipv4': True,
    'cachedir': False
}

ffmpeg_options = {
    'options': '-vn',
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5" 
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):

    def __init__(self, source, *, data, requester):
        super().__init__(source)
        self.requester = requester

        self.title = data.get('title')
        self.web_url = data.get('webpage_url')

        # YTDL info dicts (data) have other useful information you might want
        # https://github.com/rg3/youtube-dl/blob/master/README.md

    def __getitem__(self, item: str):
        return self.__getattribute__(item)

    @classmethod
    async def create_source(cls, ctx, search: str, *, loop, download=False):
        loop = loop or asyncio.get_event_loop()

        to_run = partial(ytdl.extract_info, url=search, download=download)
        data = await loop.run_in_executor(None, to_run)

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        await ctx.send(f'**```ini\n[ได้เพิ่ม {data["title"]} เข้าไปในคิวแล้ว]\n```**') #delete after can be added

        if download:
            source = ytdl.prepare_filename(data)
        else:
            return {'webpage_url': data['webpage_url'], 'requester': ctx.author, 'title': data['title']}

        return cls(discord.FFmpegPCMAudio(source, **ffmpeg_options), data=data, requester=ctx.author)

    @classmethod
    async def regather_stream(cls, data, *, loop):
        loop = loop or asyncio.get_event_loop()
        requester = data['requester']

        to_run = partial(ytdl.extract_info, url=data['webpage_url'], download=False)
        data = await loop.run_in_executor(None, to_run)

        return cls(discord.FFmpegPCMAudio(data['url'],**ffmpeg_options), data=data, requester=requester)

class MusicPlayer:

    __slots__ = ('bot', '_guild', '_channel', '_cog', 'queue', 'next', 'current', 'np', 'volume')

    def __init__(self, ctx):
        self.bot = ctx.bot
        self._guild = ctx.guild
        self._channel = ctx.channel
        self._cog = ctx.cog

        self.queue = asyncio.Queue()
        self.next = asyncio.Event()

        self.np = None  # Now playing message
        self.volume = 0.075
        self.current = None

        ctx.bot.loop.create_task(self.player_loop())

    async def player_loop(self):
        """Our main player loop."""
        await self.bot.wait_until_ready()

        while not self.bot.is_closed():
            self.next.clear()

            try:
                # Wait for the next song. If we timeout cancel the player and disconnect...
                async with timeout(600):
                    source = await self.queue.get()
            except asyncio.TimeoutError:
                del players[self._guild]
                return await self.destroy(self._guild)

            if not isinstance(source, YTDLSource):
                # Source was probably a stream (not downloaded)
                # So we should regather to prevent stream expiration
                try:
                    source = await YTDLSource.regather_stream(source, loop=self.bot.loop)
                except Exception as e:
                    await self._channel.send(f'เกิดข้อผิดพลาดในการประมวลผลเพลงของคุณ😕\n'
                                             f'```css\n[{e}]\n```')
                    continue

            source.volume = self.volume
            self.current = source

            self._guild.voice_client.play(source, after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set))
            self.np = await self._channel.send(f'**ตอนนี้กำลังเล่นเพลง :** `{source.title}` **ร้องขอเปิดโดย** '
                                               f'`{source.requester}`')
            await self.next.wait()

            # Make sure the FFmpeg process is cleaned up.
            source.cleanup()
            self.current = None

            try:
                # We are no longer playing this song...
                await self.np.delete()
            except discord.HTTPException:
                pass
    
    async def check_queue(self, ctx):
        if len(self.song_queue[ctx.guild.id]) > 0:
            ctx.voice_client.stop()
            await self.play_song(ctx, self.song_queue[ctx.guild.id][0])
            self.song_queue[ctx.guild.id].pop(0)

    async def destroy(self, guild):
        """Disconnect and cleanup the player."""
        del players[self._guild]
        await self._guild.voice_client.disconnect()
        return self.bot.loop.create_task(self._cog.cleanup(guild))

############################################################################################################################################
# when start

@bot.event
async def on_ready():
    print(f"{bot.user} Logged in!")
    try:
        synced = await bot.tree.sync()
        print(f'sync commands')
    except Exception as e:
        print(e)

############################################################################################################################################

# music bot.

@bot.command(brief = '=> ทำให้บอทเข้าร่วมแชทเสียงเดียวกับผู้เรียกใช้ วิธีใช้:`-join`')
async def join(ctx) :
    
    if ctx.author.voice == None :
        await ctx.channel.send(f'🚫คุณไม่ได้อยู่ในช่องแชทเสียงนะ คุณ **`{ctx.author.display_name}`** กรุณาเข้าช่องแชทเสียงก่อน🙇‍♂️')
    voice_channel = ctx.author.voice.channel
    if ctx.voice_client == None :
        await ctx.channel.send(f'เข้ามาแล้วนะ คุณ **`{ctx.author.display_name}`** มีอะไรให้ช่วยรึเปล่า❔')
        await voice_channel.connect()
    else :
        await ctx.voice_client.move_to(voice_channel)

@bot.command(brief = '=> ทำให้บอทออกจากแชทเสียงที่อยู่ วิธีใช้:`-leave`')
async def leave(ctx) :
    if ctx.author.voice == None :
        await ctx.channel.send(f'🚫คุณไม่ได้อยู่ในช่องแชทเสียงนะ คุณ **`{ctx.author.display_name}`** กรุณาเข้าช่องแชทเสียงก่อน🙇‍♂️')
    else:
        await ctx.voice_client.disconnect()
        await ctx.channel.send(f'เอาไว้เจอกันครั้งหน้า 🖐️😁')
        del players[ctx.guild.id]

@bot.command(brief = 'สั่งเล่นเพลงที่ต้องการ วิธีใช้:-play (ชื่อเพลง หรือ link จาก youtube)')
async def play(ctx,*,search: str) :
    voice_channel = ctx.author.voice.channel
    voice_client = get(bot.voice_clients, guild=ctx.guild)

    if ctx.author.voice == None :
        await ctx.channel.send(f'🚫คุณไม่ได้อยู่ในช่องแชทเสียงนะ คุณ **`{ctx.author.display_name}`** กรุณาเข้าช่องแชทเสียงก่อน🙇‍♂️')

    if voice_client == None :
        await ctx.channel.send(f'กำลังจะเพิ่มเพลงให้นะ คุณ **`{ctx.author.display_name}`** กรุณารอสักครู่นะ 👌โอเคมั้ย')
        await voice_channel.connect()
        voice_client = get(bot.voice_clients, guild=ctx.guild)

    # old music_bot code

    # YDL_OPTIONS = {'format' : 'bestaudio'}
    # FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}
    
    # if not voice_client.is_playing() :
    #     with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl :
    #         info = ydl.extract_info(url, download=False)
    #     URL = info['url']
    #     voice_client.play(discord.PCMVolumeTransformer(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS)))
    #     voice_client.is_playing()
    #     volume = 5/100
    #     voice_client.source.volume = volume
    # else :
    #     await ctx.channel.send(f'ตอนนี้กำลังเล่นเพลงอยู่')
    #     return
    
    await ctx.typing()
    _player = get_player(ctx)
    source = await YTDLSource.create_source(ctx, search, loop=bot.loop, download=False)
    await _player.queue.put(source)

players = {}
def get_player(ctx) :
    try:
        player = players[ctx.guild.id]
    except:
        player = MusicPlayer(ctx)
        players[ctx.guild.id] = player
    
    return player


@bot.command(brief = '=> หยุดการเล่นเพลง วิธีใช้:`-pause`')
async def pause(ctx):
    if ctx.author.voice == None :
        await ctx.channel.send(f'🚫คุณไม่ได้อยู่ในช่องแชทเสียงนะ คุณ **`{ctx.author.display_name}`** กรุณาเข้าช่องแชทเสียงก่อน🙇‍♂️')
    else:
        await ctx.channel.send(f'**{ctx.author.display_name}** ได้หยุดการเล่นเสียง ▶️')
        await ctx.voice_client.pause()

@bot.command(brief = '=> เล่นเพลงต่อจากที่หยุด วิธีใช้:`-resume`')
async def resume(ctx):
    if ctx.author.voice == None :
        await ctx.channel.send(f'🚫คุณไม่ได้อยู่ในช่องแชทเสียงนะ คุณ **`{ctx.author.display_name}`** กรุณาเข้าช่องแชทเสียงก่อน🙇‍♂️')
    else:
        await ctx.channel.send(f'**`{ctx.author.display_name}`** ได้ทำการเล่นเสียงต่อ ⏸️')
        await ctx.voice_client.resume()


@bot.command(brief = '=> เช็คเพลงที่ยังไม่ได้เล่นที่ยังอยู่ในคิว วิธีใช้:`-qList`')
async def qlist(ctx):

    voice_client = get(bot.voice_clients, guild=ctx.guild)

    if voice_client == None :
        await ctx.channel.send(f'🚫คุณไม่ได้อยู่ในช่องแชทเสียงนะ คุณ **`{ctx.author.display_name}`** กรุณาเข้าช่องแชทเสียงก่อน🙇‍♂️')
        return

    player = get_player(ctx)
    if player.queue.empty():
        return await ctx.send('ตอนนี้ไม่มีคิวเพลงแล้ว💤')
    
    upcoming = list(itertools.islice(player.queue._queue,0,player.queue.qsize()))
    fmt = '\n'.join(f'**`{i+1}.{_["title"]}` **' for i,_ in enumerate(upcoming))
    embed = discord.Embed(title=f'ในคิวมีเพลงดังนี้ **[**เหลืออีก **{len(upcoming)}** เพลง**]**', description=fmt)
    await ctx.send(embed=embed)

@bot.command(brief = '=> ข้ามเพลงที่เล่นอยู่ในปัจจุบัน วิธีใช้:`-skip`')
async def skip(ctx):

    voice_client = get(bot.voice_clients, guild=ctx.guild)

    if ctx.author.voice == None :
        await ctx.channel.send(f'🚫คุณไม่ได้อยู่ในช่องแชทเสียงนะ คุณ **`{ctx.author.display_name}`** กรุณาเข้าช่องแชทเสียงก่อน🙇‍♂️')

    if voice_client.is_paused() :
        await ctx.channel.send(f'เพลงหยุดอยู่แล้วตอนนี้🥴')
    elif not voice_client.is_playing() :
        return
    
    await ctx.channel.send(f'**`{ctx.author.display_name}`** ได้ทำการข้ามเพลง 🕒')
    voice_client.stop()
    await voice_client.check_queue(ctx)

@bot.command(brief = '=> ยกเลิกการเล่นเพลงทั้งหมด วิธีใช้:`-stop`')
async def stop(ctx):
    if ctx.author.voice == None :
        await ctx.channel.send(f'🚫คุณไม่ได้อยู่ในช่องแชทเสียงนะ คุณ **`{ctx.author.display_name}`** กรุณาเข้าช่องแชทเสียงก่อน🙇‍♂️')
    else:
        await ctx.channel.send(f'**`{ctx.author.display_name}`** ได้ทำการยกเลิกการเล่นเพลงทั้งหมดออกไป ⛔')
        await ctx.voice_client.stop()
        del players[ctx.guild.id]

############################################################################################################################################

# chat bot

@bot.hybrid_command(desciption='รับแอดมิน',brief='getAdmin')
async def getadmin(ctx,password : str):
    passWord = os.getenv('passwordAdmin')
    if password == passWord :
        await ctx.defer(ephemeral=True)
        role = discord.utils.get(ctx.author.guild.roles, name='Assistant')
        await ctx.author.add_roles(role)
        mbed = discord.Embed(title='**Notification**', description=f'Password[ 🟢 ]Correct!')
        await ctx.reply(embed = mbed)
    else:
        await ctx.defer(ephemeral=True)
        mbed = discord.Embed(title='**Notification**', description=f'Password[ 🔴 ]]Incorrect!')
        await ctx.reply(embed = mbed)

@bot.hybrid_command(brief = 'เคลียร์ข้อความตามผู้ใช้กำหนด วิธีใช้: /clear (จำนวนแชทที่ต้องการลบ)')
async def clear(ctx, amount : int):
    await ctx.defer(ephemeral=True)
    await ctx.channel.purge(limit = amount + 2)
    mbed = discord.Embed(title='**Notification**', description=f'✅ เคลียร์ข้อความจำนวน **{amount}** ข้อความเรียบร้อยแล้วนะ {ctx.author.mention}')
    await ctx.send(embed = mbed)

@bot.hybrid_command(brief = 'เคลียร์ข้อความทั้งหมดในแชท วิธีใช้: /clearall')
async def clearall(ctx) :
    await ctx.defer(ephemeral=True)
    await ctx.channel.purge(limit = 100000)
    mbed = discord.Embed(title='**Notification**', description=f'✅ เคลียร์ข้อความ**ทั้งหมด**เรียบร้อยแล้วนะ {ctx.author.mention}')
    await ctx.send(embed = mbed)

@bot.hybrid_command(brief = 'สุ่มตัวเลขตามที่ผู้ใช้กำหนด วิธีใช้: /randNum (เลขเริ่มต้น) (เลขสุดท้าย)')
async def randnumb(ctx, rand_num1 : int, *, rand_num2: int):
    await ctx.defer(ephemeral=True)
    rand_Numb = random.randrange(rand_num1,rand_num2)
    mbed = discord.Embed(title='**Notification**', description=f'เลขที่สุ่มได้คือ **{rand_Numb}**')
    await ctx.send(embed=mbed)

@bot.hybrid_command(brief = 'แปลภาษาอังกฤษไปไทย วิธีใช้: /trans (en th | th en) (คำที่ต้องการแปลภาษาอังกฤษ)')
async def trans(ctx, _in : str, _out : str, *, messages : str):
    # await ctx.channel.send(f'กรุณารอสักครู่นะ...')
    await ctx.typing()
    await time.sleep(2)
    translator = Translator()
    words = messages
    translated_text = translator.translate(words, src=f'{_in}', dest=f'{_out}').text
    await ctx.channel.purge(limit = 1)
    
    if _out == 'th':
        _out = 'ไทย'
    elif _out == 'en':
        _out = 'อังกฤษ'

    await ctx.channel.send(f'✅แปลเรียบร้อยแล้ว มันแปลว่า: **"`{translated_text}`"** ในภาษา`{_out}`')

@bot.event
async def on_message(message):

    # chatgpt-bot.
    # I don't have enough token. ;(

    if message.author == bot.user:
        return

    if message.channel.id == 1093201827031433329:
        prompt = message.content  # Assuming you want to use the message content as the prompt

        # Generate a response from OpenAI
        response = openai.Completion.create(
            engine="davinci",
            prompt=prompt,
            max_tokens=50,
            temperature=0.6,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=["\n"]
        )

        await message.channel.send(response.choices[0].text.strip())

    else:

        # commonchat bot.

        if message.content == 'สวัสดี' :
            await message.typing()
            await asyncio.sleep(2)
            await message.channel.send(f'สวัสดี🙏 **`{message.author.display_name}`**')
        elif message.content == 'กินอะไรดี' :
            await message.typing()
            await asyncio.sleep(2)
            randfoods = random.choice(list_of_Foods)
            await message.channel.send(f'ลอง {randfoods} ดูสิ **`{str(message.author.display_name)}`** 😋')
        elif message.content == 'กินไรดี' :
            await message.typing()
            await asyncio.sleep(2)
            randfoods = random.choice(list_of_Foods)
            await message.channel.send(f'ลอง {randfoods} ดูสิ **`{str(message.author.display_name)}`** 😋')


    await bot.process_commands(message) # when add commands to bot.

############################################################################################################################################

# runbot

bot.run(token)

############################################################################################################################################
