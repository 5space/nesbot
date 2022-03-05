
from modules.games.util.game import TurnBasedGame, Rules, DEFAULT_GAME_TOKENS


C4_EMPTY = 0
C4_RED = 1
C4_BLUE = 2


C4_NUMBERS = ["1\N{COMBINING ENCLOSING KEYCAP}",
              "2\N{COMBINING ENCLOSING KEYCAP}",
              "3\N{COMBINING ENCLOSING KEYCAP}",
              "4\N{COMBINING ENCLOSING KEYCAP}",
              "5\N{COMBINING ENCLOSING KEYCAP}",
              "6\N{COMBINING ENCLOSING KEYCAP}",
              "7\N{COMBINING ENCLOSING KEYCAP}",
              "8\N{COMBINING ENCLOSING KEYCAP}",
              "9\N{COMBINING ENCLOSING KEYCAP}",
              "\N{KEYCAP TEN}"]


class ConnectFourRules(Rules):

    keys = ["width", "height", "length"]

    def __init__(self):
        super().__init__()
        self._width = 7
        self._height = 6
        self._length = 4

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        if not value.isdigit() or int(value) not in range(1, 11):
            raise ValueError("Invalid value (must be between 1 and 10)")
        self._width = int(value)

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        if not value.isdigit() or int(value) not in range(1, 11):
            raise ValueError("Invalid value (must be between 1 and 10)")
        self._height = int(value)

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, value):
        if not value.isdigit() or int(value) not in range(3, 6):
            raise ValueError("Invalid value (must be between 3 and 5)")
        self._length = int(value)


class ConnectFour(TurnBasedGame):

    min_players = 2
    max_players = 2
    name = "Connect Four"

    def __init__(self, handler, channel, players):
        super().__init__(handler, channel, players)
        self.rules = ConnectFourRules()
        self.board = list()

        self.player_icons = DEFAULT_GAME_TOKENS

    async def start(self):
        await super().start()
        self.board = [[0 for _ in range(self.rules.height)] for _ in range(self.rules.width)]
        self.player_icons = [self.handler.bot.user_config.get(self.players[i].id, "game-emote") or self.player_icons[i]
                             for i in range(len(self.players))]
        await self.display()

    def check_win(self):
        for x in range(self.rules.height-self.rules.length+1):
            for y in range(self.rules.width):
                if self.board[y][x] != 0 and len(set(self.board[y][x+n] for n in range(self.rules.length))) == 1:
                    return self.board[y][x]
        for x in range(self.rules.height):
            for y in range(self.rules.width-self.rules.length+1):
                if self.board[y][x] != 0 and len(set(self.board[y+n][x] for n in range(self.rules.length))) == 1:
                    return self.board[y][x]
        for x in range(self.rules.height-self.rules.length+1):
            for y in range(self.rules.width-self.rules.length+1):
                if self.board[y][x] != 0 and len(set(self.board[y+n][x+n] for n in range(self.rules.length))) == 1:
                    return self.board[y][x]
        for x in range(self.rules.height-self.rules.length+1):
            for y in range(self.rules.width-self.rules.length+1):
                if self.board[y][x+self.rules.length-1] != 0 and len(set(self.board[y+n][x+self.rules.length-n-1]
                                                                         for n in range(self.rules.length))) == 1:
                    return self.board[y][x+self.rules.length-1]
        return 0

    def get_board(self):
        msg = "".join(C4_NUMBERS[:self.rules.width]) + "\n"
        for x in range(self.rules.height-1, -1, -1):
            for y in range(self.rules.width):
                cell = self.board[y][x]
                if cell == C4_EMPTY:
                    msg += "\N{WHITE LARGE SQUARE}"
                else:
                    msg += self.player_icons[cell - 1]
            msg += "\n"
        return msg

    def get_key(self):
        return " ".join(f"{self.player_icons[i]} **{self.players[i].name}**" for i in range(len(self.players)))

    def get_display(self):
        return f"It is currently **{self.get_turn().name}'s** turn.\n" + self.get_board() + "\n" + self.get_key()

    async def display(self):
        await self.send(self.get_display())

    async def play_coaster(self, player, row):
        await self.reset_timeout()
        for index, cell in enumerate(self.board[row]):
            if cell == 0:
                self.board[row][index] = self.turn + 1
                win = self.check_win()
                if win > 0:
                    self.winner = self.players[win-1]
                    await self.end()
                    return
                if not any(0 in row for row in self.board):
                    await self.end()
                    return
                self.turn += 1
                self.turn %= len(self.players)
                await self.send(f"**{player.name}** played a coaster in column {row + 1}.\n"
                                f"It is now **" + self.get_turn().name + "'s** turn.\n\n"
                                + self.get_board() + "\n" + self.get_key())
                return
        await self.send("Invalid move.")

    async def on_message(self, message):
        if message.author != self.get_turn():
            return
        if not message.content.isnumeric() or int(message.content) not in range(1, self.rules.width+1):
            return
        await self.play_coaster(message.author, int(message.content) - 1)

    async def end(self):
        await super().end()
        if self.winner is None:
            await self.send("There was a tie and nobody received points.\n\n" + self.get_board())
        else:
            # self.handler.add_tokens(self.channel.guild, self.winner.id, 5)
            await self.send(f"Winner: **{self.winner.name}**\n\n" + self.get_board())
