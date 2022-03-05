import html
import json
import random

import aiohttp

from modules.games.util.game import RoundBasedGame

LETTER_CHOICES = ["\N{REGIONAL INDICATOR SYMBOL LETTER A}",
                  "\N{REGIONAL INDICATOR SYMBOL LETTER B}",
                  "\N{REGIONAL INDICATOR SYMBOL LETTER C}",
                  "\N{REGIONAL INDICATOR SYMBOL LETTER D}"]


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def gen_quiz_questions(amount):
    async with aiohttp.ClientSession() as session:
        response = await fetch(session, f"https://opentdb.com/api.php?amount={amount}")
        return json.loads(html.unescape(response.replace("&quot;", "\\\"")))["results"]


class Quiz(RoundBasedGame):

    min_players = 1
    max_players = 5
    name = "Quiz"

    def __init__(self, handler, channel, players):
        super().__init__(handler, channel, players)

        self.questions = {}
        self.scores = {}

    async def make_questions(self):
        questions = await gen_quiz_questions(5)
        new_questions = []
        for q in questions:
            order = q["incorrect_answers"] + [q["correct_answer"]]
            random.shuffle(order)
            answer = order.index(q["correct_answer"])
            new_questions.append({"category": q["category"],
                                  "difficulty": q["difficulty"],
                                  "type": q["type"],
                                  "question": q["question"],
                                  "choices": order,
                                  "answer": answer})
        self.questions = new_questions

    def get_current_question(self):
        return self.questions[self.round]

    def inc_score(self, player):
        if player not in self.scores:
            self.scores[player] = 1
        else:
            self.scores[player] += 1

    def get_display(self):
        question = self.get_current_question()
        lines = "\n".join(LETTER_CHOICES[i] + " " + str(c) for i, c in enumerate(question["choices"]))
        return f"Question {self.round+1}/{len(self.questions)} ({question['category']}):\n" \
               f"Difficulty: {question['difficulty']}\n" \
               f"{question['question']}\n{lines}"

    async def start(self):
        await self.make_questions()
        await super().start()
        await self.display()

    async def on_message(self, message):
        await super().on_message(message)
        if message.content not in "abcd":
            return
        index = "abcd".index(message.content)
        if message.author in self.players_done:
            await self.send(f"You have already guessed.")
            return
        if self.get_current_question()["answer"] == index:
            self.inc_score(message.author)
            await self.on_player_finish(message.author)
            if self.round >= len(self.questions):
                await self.end()
            else:
                await self.send(f"{message.author.mention} got the question right!\n"
                                + self.get_display())
        else:
            await message.add_reaction("\N{CROSS MARK}")
            await self.on_player_finish(message.author)
            if self.round >= len(self.questions):
                if len(self.players) > 1:
                    await self.send("All players have gotten the question wrong, skipping:")
                await self.end()
            else:
                if len(self.players) > 1:
                    await self.send("All players have gotten the question wrong, skipping:\n"
                                    + self.get_display())
                else:
                    await self.display()

    async def end(self):
        await super().end()
        sorted_scores = sorted(self.scores.items(), key=lambda kv: kv[1])
        if len(sorted_scores) == 0:
            await self.send("There is no winner as nobody got a question correct.")
        else:
            self.winner = sorted_scores[0][0]
            # self.handler.add_tokens(self.channel.guild, self.winner.id, 10)
            await self.send(f"Winner: **{self.winner.name}** ({sorted_scores[0][1]} points).")

    async def display(self):
        await self.send(self.get_display())
