import math

import chess
import discord

from modules.games.util.game import TurnBasedGame, Rules


class ChessRules(Rules):

    keys = ["chess960"]

    def __init__(self):
        super().__init__()
        self._chess960 = False

    @property
    def chess960(self):
        return self._chess960

    @chess960.setter
    def chess960(self, value):
        try:
            value = ["true", "false"].index(value.lower()) == 0
        except ValueError:
            raise ValueError("Invalid value (must be either true or false)")
        self._chess960 = value


class Chess(TurnBasedGame):

    min_players = 2
    max_players = 2
    name = "Chess"

    def __init__(self, handler, channel, players):
        super().__init__(handler, channel, players)
        self.rules = ChessRules()
        self.board = chess.Board()
        self.moves = []
        self.draw_requests = []
        self.on_draw_cooldown = []

        self.winner = None

    def parse_move(self, string):
        move = None
        try:
            move = self.board.parse_san(string)
        except Exception:
            pass
        try:
            move = self.board.parse_uci(string)
        except Exception:
            pass
        return move

    def board_embed(self):
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_image(url="http://www.fen-to-image.com/image/48/" + self.board.board_fen())
        return embed

    def can_claim_draw(self):
        if self.board.can_claim_draw():
            return True
        if self.board.can_claim_fifty_moves():
            return True
        if self.board.can_claim_threefold_repetition():
            return True
        return False

    async def start(self):
        if len(self.players) < 2:
            await self.add_ai_opponent(name="Opponent")
        await super().start()
        await self.display()

    def get_display(self):
        lines = f"Move {math.floor(len(self.moves)/2)+1}, {['White', 'Black'][self.turn]} to Move"
        return lines

    async def display(self):
        await self.send(self.get_display(), embed=self.board_embed())

    async def play_move(self, player, move):
        self.board.push(move)
        self.moves.append(move)
        self.turn += 1
        self.turn %= len(self.players)
        self.draw_requests = []
        self.on_draw_cooldown = []
        if self.board.is_checkmate():
            self.winner = player
            await self.end()
            return
        elif self.board.is_stalemate():
            await self.end()
            return
        elif self.board.is_insufficient_material():
            await self.end()
            return
        elif self.board.is_seventyfive_moves():
            await self.end()
            return
        elif self.board.is_fivefold_repetition():
            await self.end()
            return
        elif self.board.is_check():
            await self.send(f"**{player.name}** played the move {move}. ***CHECK!***\n\n"
                            + self.get_display(), embed=self.board_embed())
        else:
            await self.send(f"**{player.name}** played the move {move}.\n\n"
                            + self.get_display(), embed=self.board_embed())

    async def on_message(self, message):
        if message.author != self.get_turn():
            return
        move = self.parse_move(message.content)
        if move is None:
            return
        if not self.board.is_legal(move):
            await self.send("Invalid move.")
            return
        await self.play_move(message.author, move)

    async def end(self):
        await super().end()
        if self.winner is None:
            await self.send("The game was drawn.\n\n",
                            embed=self.board_embed())
        else:
            # self.handler.add_tokens(self.channel.guild, self.winner.id, 50)
            await self.send(f"Winner: **{self.winner.name}**\n\n",
                            embed=self.board_embed())
