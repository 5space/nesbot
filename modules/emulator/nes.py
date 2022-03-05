import discord
from discord.ui import Button, View
from nes import NES

from PIL import Image
from io import BytesIO


K_A = 0
K_B = 1
K_SELECT = 2
K_START = 3
K_UP = 4
K_DOWN = 5
K_LEFT = 6
K_RIGHT = 7


async def get_acceptable_url(file, channel):
    message = await channel.send(file=file)
    return message.attachments[0].url


def array_to_discord_file(arr):
    img = Image.fromarray(arr).resize((720, 672), resample=Image.NEAREST)
    fp = BytesIO()
    img.save(fp, format="JPEG")
    fp.seek(0)
    return discord.File(fp, filename="frame.png")


class ToggleButton(Button):

    def __init__(self, id, *args, **kwargs):
        super().__init__(*args, **kwargs, style=discord.ButtonStyle.primary)
        self.toggled = False
        self.callback = self.toggle
        self.id = id

    async def toggle(self, itc):
        if itc.user != self.view.session.user: return
        self.toggled = not self.toggled
        if self.toggled:
            self.style = discord.ButtonStyle.success
        else:
            self.style = discord.ButtonStyle.primary
        self.view.state[self.id] = self.toggled
        await self.view.update()


class ControllerView(View):

    def __init__(self, session, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.session = session
        self.state = [False for _ in range(8)]
        buttons = [Button(style=discord.ButtonStyle.secondary, label=" ", disabled=True) for _ in range(25)]

        buttons[6] = ToggleButton(emoji="⬆️", id=K_UP)
        buttons[10] = ToggleButton(emoji="⬅️", id=K_LEFT)
        buttons[12] = ToggleButton(emoji="➡️", id=K_RIGHT)
        buttons[16] = ToggleButton(emoji="⬇️", id=K_DOWN)
        buttons[20] = ToggleButton(emoji="<:ethangaming:805188408083349524>", id=K_SELECT)
        buttons[22] = ToggleButton(emoji="<:ethansex:814043259092729876>", id=K_START)
        buttons[14] = ToggleButton(emoji=u"🇧", id=K_B)
        buttons[18] = ToggleButton(emoji=u"🇦", id=K_A)

        buttons[0] = Button(style=discord.ButtonStyle.primary, emoji="📸")
        buttons[0].callback = self.frame_callback

        for button in buttons:
            self.add_item(button)
    
    async def update(self):
        await self.session.update()

    async def frame_callback(self, itc):
        if itc.user != self.session.user: return
        await self.session.do_frame()

class NESGame:

    def __init__(self, bot, channel, user, name):
        self.bot = bot
        self.channel = channel
        self.user = user
        self.name = name
        self.message = None
        self.emulator = None
        self.embed = discord.Embed(title="Current Frame")
        self.embed.set_image(url="https://cdn.discordapp.com/attachments/851697058057814068/851701176072011806/frame.jpg")
        self.controller = ControllerView(self)
    
    async def start(self):
        self.message = await self.channel.send(embed=self.embed, view=self.controller)
        self.emulator = NES("roms\\" + self.name + ".nes")
    
    async def update(self):
        await self.message.edit(embed=self.embed, view=self.controller)

    async def do_frame(self):
        buffer = self.emulator.run_frame_headless(run_frames=60, controller1_state=self.controller.state)
        file = array_to_discord_file(buffer)
        url = await get_acceptable_url(file, self.bot.dump_channel)
        self.embed.set_image(url=url)
        await self.update()