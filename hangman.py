from random import randint
from smtplib import SMTP_SSL
from os import environ
from email.message import EmailMessage


# multi-player hangman game, at least 2 players needed to play. There is no upper bounds 
# program will ask for the number of players. Every letter found will be 10 points. So if ther will be 3 letters that has been guessed corretly, this will result in
# 30 points. If a word is know correctly, this will give 100 points irrelevant of how many letters left. Each player will have five chances for each turn
# those will be right-left arms, right-left legs and the head. For each new word, the chances of palyers will be renewed. A game will last 2n + 1 turns whre n is the 
# number of the players
# also each player should enter their email address to send them the results afterwards
# if a player knows the word n + 1 times, additional 100 points will be added.

class Hangman:
    body = ["left leg", "right leg", "left arm", "right arm", "head"]
    body_parts_count = 5
    def renew(self):
        self.body = ["left leg", "right leg", "left arm", "right arm", "head"]
    def reduce(self):
        self.body.pop(0)
        self.body_parts_count -= 1
    def loss(self):
        self.body = []

class Player:
    points = 0
    words_guess_correctly = 0
    player_name = ""
    def __init__(self):
        self.hangman = Hangman()
    def pointArranger(self, gained_points):
        self.gained_points = gained_points
        self.points += self.gained_points
    # method for counting words_guess_correctly
    def wordCount(self):
        self.words_guess_correctly += 1
    def totalPoints(self):
        self.points += 100 * self.words_guess_correctly

class EmailSender:
    SENDER = environ.get("EMAIL_ADDRESS")
    PASWORD = environ.get("EMAIL_PASSWORD")
    # to send email the user email address has been taken from
    # the environment variables. To use this feautre it is necessary to
    # create two seperate env variables as SENDER and PASSWORD
    # respecitvely hodls the email account and the passwpord
    def __init__(self, players_points, players_ranking, receiver):
        self.players_points = players_points
        self.players_ranking = players_ranking
        self.receiver = receiver
    def send(self):
        self.message = EmailMessage()
        self.message['Subject'] = "Results of the hangman game"
        self.message.set_content("")
        self.message['From'] = self.SENDER
        self.message['To'] = self.receiver
        with SMTP_SSL('smtp@gmail.com', 465) as smtp:
            smtp.login(self.SENDER, self.PASWORD)
            smtp.send_message(self.message)
    def __repr__(self):
        return ("The scores sent to the ", self.receiver)

def checkSameOrNot(list, word):
    if len(list) != 0:
        for index, element in enumerate(list):
            if element is word[index]:
                continue
            else:
                return False
        return True
    else:
        return False

def indexFinder(letter, word):
    index_list = []
    for index, element in enumerate(word):
        if letter is element:
            index_list.append(index)
    return index_list

def atLeastOnePlayer(players):
    for player in players:
        if len(player.hangman.body) > 0:
            return True
    return False

def empty_index_delete(list):
    for index, element in enumerate(list):
        if element == "":
            del list[index]
            return 

def rank_players(players):
    players_ranking = []
    for i in range(len(players)):
        for j in range(len(players)):
            pass
    return players_ranking
    # TODO for ranking out players

def find_winner(players):
    max = players[0].points
    winners = []
    for player in players:
        if player.points > max:
            max = player.points
    for player in players:
        if player.points == max:
            winners.append(player.player_name)
    return winners

def play():
    while(True):
        number_of_players = int(input("Please enter the number of players: "))
        print("\n")
        if number_of_players >= 2:
            break
        else:
            print("Please enter at least 2 as number of the players")
    players = [Player() for i in range(number_of_players)]
    for p in range(number_of_players):
        text = "Enter the nickname for the player {number}: ".format(number=p+1)
        nickname = input(text)
        players[p].player_name += nickname
    number_of_games = 2 * number_of_players + 1
    words = ["charisma", "alter", "redemption", "hobbit", "elves", "wine",
            "incomprehensibility", "hippopotomonstrosesquippedaliophobia",
            "target", "emission", "absurd", "syndrome", "byte", "rhythm",
            "subway", "squdgy"]
    random_index_of_words = randint(0, len(words) - 1)

    print("Let's start the game\n")
    for i in range(number_of_games):
        print("Please guess a letter or a word. If the input is greater or equal to 2, it will considered as a sentence")
        found_word = ["" for i in range(len(words[random_index_of_words]))]
        index_list = []
        for i in range(len(words[random_index_of_words])):
            print("_ ", end=" ")
        print("\n")
        while not(checkSameOrNot(found_word, words[random_index_of_words])):
            for player in range(number_of_players):
                if players[player].hangman.body_parts_count < 1:
                    continue
                elif atLeastOnePlayer(players):
                    entry = input("Turn of player {player_name}, please guess a letter or a word: ".format(player_name=players[player].player_name))
                    if len(entry) > 1:
                        if entry == words[random_index_of_words]:
                            print("Player {player} has guessed the word correctly. Congrats! Earned +100 points".format(player=players[player].player_name))
                            words.remove(entry)
                            players[player].pointArranger(100)
                            players[player].wordCount()
                        else:
                            print("Wrong guess, player {player} is out for this word".format(player=players[player].player_name))
                            players[player].hangman.loss()
                    elif len(entry) == 1:
                        if entry in words[random_index_of_words]:
                            index_list = indexFinder(entry, words[random_index_of_words])
                            for index in index_list:
                                players[player].pointArranger(10)
                                found_word.insert(index, entry)
                                empty_index_delete(found_word)
                            print("Good guess!")
                            for i in found_word:
                                if i == "":
                                    print("_ ", end="")
                                else:
                                    print(i, end="")
                            print(" \n", end="")
                        else:
                            print("Wrong guess")
                            players[player].hangman.reduce()
                    else:
                        print("Player {player} has passed the turn, -10 points".format(player=players[player].player_name))
                        players[player].pointArranger(-10)
                else:
                    print("this turn ends, the word is not found")
            print("This word is completed")
        words.pop(random_index_of_words)
    
    for player in players:
        player.totalPoints()
    winners = find_winner(players)
    players_ranking = rank_players(players)

    
play()