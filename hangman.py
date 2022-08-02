from random import randint, random
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

class EmailSender:
    # TODO add env varaibles and edit the content of the message
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
        for i in range(len(words[random_index_of_words])):
            print("_ ", end=" ")
        print("\n")
        break


play()