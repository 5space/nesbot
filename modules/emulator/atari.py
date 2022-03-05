import discord
from discord.ui import Button, View
from .pytari2600.pytari2600 import new_atari

from PIL import Image
from io import BytesIO
import pygame
import numpy


K_A = 0
K_UP = 1
K_DOWN = 2
K_LEFT = 3
K_RIGHT = 4


async def get_acceptable_url(file, channel):
    message = await channel.send(file=file)
    return message.attachments[0].url


def arr_to_discord_file(arr):
    
    rg, b = divmod(arr, 256)
    r, g = divmod(rg, 256)
    arr2 = numpy.stack([r, g, b], axis=-1)

    img = Image.fromarray(arr2.astype("uint8"))
    x, y = img.size
    fp = BytesIO()
    img.crop((0, 0, x, 260)).resize((4*x, 520), resample=Image.NEAREST).save(fp, format="PNG")
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
        self.state = [False for _ in range(5)]
        buttons = [Button(style=discord.ButtonStyle.secondary, label=" ", disabled=True) for _ in range(25)]

        buttons[7] = ToggleButton(emoji="⬆️", id=K_UP)
        buttons[11] = ToggleButton(emoji="⬅️", id=K_LEFT)
        buttons[13] = ToggleButton(emoji="➡️", id=K_RIGHT)
        buttons[17] = ToggleButton(emoji="⬇️", id=K_DOWN)
        buttons[20] = ToggleButton(emoji="🔴", id=K_A)

        buttons[0] = Button(style=discord.ButtonStyle.primary, emoji="📸")
        buttons[0].callback = self.frame_callback

        for button in buttons:
            self.add_item(button)
    
    def get_state(self):
        swcha = 0xFF
        if self.state[K_RIGHT]: swcha ^= 0x80
        if self.state[K_LEFT]: swcha ^= 0x40
        if self.state[K_DOWN]: swcha ^= 0x20
        if self.state[K_UP]: swcha ^= 0x10
        input7 = 0xFF
        if self.state[K_A]: input7 = 0x7F
        return swcha, input7

    async def update(self):
        await self.session.update()

    async def frame_callback(self, itc):
        if itc.user != self.session.user: return
        await self.session.do_frame()

class AtariGame:

    def __init__(self, bot, channel, user, name):
        self.bot = bot
        self.channel = channel
        self.frame = 1
        self.user = user
        self.name = name
        self.message = None
        self.emulator = None
        self.embed = discord.Embed(title="Frame 1")
        self.embed.set_image(url="https://cdn.discordapp.com/attachments/851697058057814068/851701176072011806/frame.jpg")
        self.controller = ControllerView(self)
    
    async def start(self):
        self.message = await self.channel.send(embed=self.embed, view=self.controller)
        self.emulator = new_atari("roms\\" + self.name + ".a26", headless=True)
        for _ in range(6):
            self.emulator.frame()
            self.frame += 1
    
    async def update(self):
        await self.message.edit(embed=self.embed, view=self.controller)

    async def do_frame(self):
        self.emulator.inputs.swcha, self.emulator.inputs.input7 = self.controller.get_state()

        self.emulator.frame()
        self.frame += 1
        file = arr_to_discord_file(self.emulator.stella.display_cache)
        url = await get_acceptable_url(file, self.bot.dump_channel)
        self.embed.set_image(url=url)
        self.embed.title = f"Frame {self.frame}"
        await self.update()