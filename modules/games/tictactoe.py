from modules.games.util.game import TurnBasedGame, Rules, DEFAULT_GAME_TOKENS


TTT_TILES = [["🇦", "🇧", "🇨"],
             ["🇩", "🇪", "🇫"],
             ["🇬", "🇭", "🇮"]]


class TicTacToeRules(Rules):

    keys = ["scuffed"]

    def __init__(self):
        super().__init__()
        self._scuffed = False

    @property
    def scuffed(self):
        return self._scuffed

    @scuffed.setter
    def scuffed(self, value):
        if value not in ["true", "false"]:
            raise ValueError("Invalid value (must be true or false)")
        self._scuffed = value == "true"


class TicTacToe(TurnBasedGame):

    min_players = 2
    max_players = 2
    name = "Tic-Tac-Toe"

    def __init__(self, handler, channel, players):
        super().__init__(handler, channel, players)
        self.rules = TicTacToeRules()
        self.board = list()
        self.player_icons = DEFAULT_GAME_TOKENS

    async def start(self):
        self.board = [[0 for _ in range(3)] for _ in range(3)]
        self.player_icons = [self.handler.bot.user_config.get(self.players[i].id, "game-emote") or self.player_icons[i]
                             for i in range(len(self.players))]
        await super().start()
        await self.display()

    def check_win(self):
        a, b, c = self.board[0]
        d, e, f = self.board[1]
        g, h, i = self.board[2]
        win_conditions = [(a, b, c), (d, e, f), (g, h, i), (a, d, g),
                          (b, e, h), (c, f, i), (a, e, i), (c, e, g)]
        for condition in win_conditions:
            if condition[0] != 0 and len(set(condition)) == 1:
                return condition[0]
        return 0

    def get_board(self):
        msg = str()
        for y in range(3):
            for x in range(3):
                cell = self.board[y][x]
                if cell == 0:
                    msg += TTT_TILES[y][x]
                elif cell == 1:
                    msg += self.player_icons[0]
                elif cell == 2:
                    msg += self.player_icons[1]
                msg += "\u200b"
            msg += "\n"
        return msg

    def get_key(self):
        return f"{self.player_icons[0]} **{self.players[0].name}** {self.player_icons[1]} **{self.players[1].name}**"

    def get_display(self):
        return f"It is currently **{self.get_turn().name}'s** turn.\n" + self.get_board() + "\n" + self.get_key()

    async def display(self):
        await self.send(self.get_display())

    async def play_token(self, player, x, y):
        await self.reset_timeout()
        if self.board[y][x] != 0:
            return
        self.board[y][x] = self.turn + 1
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
        await self.send(f"**{player.name}** played a token in position {'ABCDEFGHI'[3*y+x]}.\n"
                        f"It is now **" + self.get_turn().name + "'s** turn.\n\n"
                        + self.get_board() + "\n" + self.get_key())

    async def on_message(self, message):
        if message.author not in self.players:
            return
        if message.author != self.get_turn() and not self.rules.scuffed:
            return
        move = message.content.lower()
        if move not in "abcdefghi":
            return
        i = "abcdefghi".index(move)
        move_x, move_y = i % 3, i // 3
        await self.play_token(message.author, move_x, move_y)

    async def end(self):
        await super().end()
        if self.winner is None:
            await self.send("There was a tie and nobody received points.\n\n" + self.get_board())
        else:
            # self.handler.add_tokens(self.channel.guild, self.winner.id, 5)
            await self.send(f"Winner: **{self.winner.name}**\n\n" + self.get_board())
