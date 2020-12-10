import random
import itertools
import threading
import time
import sys


# Collection of colors to use for the text
class Bcolors:
    CORE_TWO = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    CORE_ONE = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# Class storing all of the stats that are printed out after each event
class Stats:
    happiness = 50
    mental_wellbeing = 50
    wealth = '↑'  # ↑ → or ↓ to signify relative money movement
    stress = 0
    days_quarantined = 0
    covid = False

    def print_stats(self):
        print(Bcolors.FAIL + 'Happiness: ' + str(self.happiness) + ' | Mental Health: ' + str(self.mental_wellbeing)
              + Bcolors.ENDC)

    def set_happiness(self, new):
        self.happiness = new

    def set_mental(self, new):
        self.mental_wellbeing = new

    def set_wealth(self, new):
        if new is 'up':
            self.wealth = '↑'
        elif new is 'down':
            self.wealth = '↓'
        else:
            self.wealth = '→'

    def set_stress(self, new):
        self.stress = new

    def set_days_quarantined(self, new):
        self.days_quarantined = new

    def set_covid(self, new):
        self.covid = new


# Creates the typing effect on the text, and allows to have different colors for the different speakers
def slow_type(speed, color, text):
    print(color)
    count = 0
    for l in text:
        if count is 100:
            sys.stdout.write(l + '\n')
            count = 0
        else:
            sys.stdout.write(l)
        sys.stdout.flush()
        time.sleep(random.random() * 7.0 / speed)
        count += 1
    print('' + Bcolors.ENDC)


# All the saved parameters the user types in
NAME = ''
ONE_WORD = ''


# Intro to the story, with a couple branching choices
def introduction():
    slow_type(100, Bcolors.CORE_ONE,
              "While I might not be one, I know a Quantum computer. Everyone says they’re so much cooler "
              "than I am, but I think it’s a bunch of BS. Sure, I only work with 0’s and 1’s and cannot change their "
              "state, but I’m old school! It just works, everyone uses me. Quantum comes along and has the "
              "oh-so-amazing idea to be both 0 and 1 at the same time. Like, does that even make sense?!? Apparently "
              "it will change everything, like being able to crack everyone’s passwords, and just like that everyone "
              "likes Quantum more now. Well, I am here to tell you that they are uncertain about EVERYTHING. Quantum "
              "couldn’t even tell you if he was looking at a 0 or 1 right now.")

    slow_type(85, Bcolors.CORE_TWO, "Excuse the First Core, he likes to go on a tangent sometimes. I’m the Second "
                                    "Core and I try and stay levelheaded. Quantum is certainly uncertain, but I think "
                                    "he’s a good guy. I just hope that everyone is able to understand why we all love him so much. He can do so much at once! I have bits and he has qubits, which can do exponentially more operations every second than my old bits. Before we go on, can I ask your name? Just go ahead and type right in the terminal window.")
    global NAME
    NAME = input()
    slow_type(105, Bcolors.CORE_ONE, "Ok, I do not always go on a tangent. I am telling you Two, we’ve gotta defend "
                                     "ourselves here! Hi, " + NAME + ", by the way. Quantum is going to make us "
                                                                     "useless soon enough. Stupid qubits in "
                                                                     "superposition that can do things we can’t. "
                                                                     "Wait, let me ask you a question too. Uhmmm, "
                                                                     "what is your social security number? ")
    slow_type(85, Bcolors.CORE_TWO, "One!!! We talked about this. No one wants to tell us that, okay? ")
    slow_type(105, Bcolors.CORE_ONE, "Fine. I still can’t get over the fact that Quantum is not certain of anything, "
                                     "ever. Wouldn’t that make you go crazy? Have you ever been as uncertain as "
                                     "Quantum? (Yes/No)")
    choice1 = input()
    if choice1.lower() == ('yes' or 'y'):
        slow_type(105, Bcolors.CORE_ONE, "Oh that’s right, humanity is dealing with a pandemic right now. I’ve heard "
                                         "that is a pretty big deal out there. You know, I got a virus once too, "
                                         "when someone tried downloading a movie. Just pay for Netflix like the rest "
                                         "of the schmucks out there and keep me fresh.")
    else:
        slow_type(85, Bcolors.CORE_TWO, "One, stop messing with them. Obviously they’re going through a pandemic and "
                                        "there might be lots of things that are on their nerves right now. ")

    slow_type(85, Bcolors.CORE_TWO, "This year must have been so uncertain for all you humans. There is actually a "
                                    "simulation I have that we could run, it shows how some of the major events of "
                                    "the year may have impacted people. You’ll draw events randomly and I’ll choose "
                                    "one of a few related scenarios for you to ponder. It might not describe you or "
                                    "anyone you know, but someone during the uncertainty of the pandemic has "
                                    "certainly been in that situation. You can also shoot for a high score with the "
                                    "built in Lifestyle Stats! What do you say, would you like to try it out! (Yes/No")
    choice2 = input()
    global ONE_WORD
    if choice2.lower() == ('yes' or 'y'):
        slow_type(85, Bcolors.CORE_TWO, "Great! Let’s get started. To calibrate, you type one adjective that ends in "
                                        "-ing that describes 2020 best for you.")
        ONE_WORD = input()
    else:
        slow_type(85, Bcolors.CORE_TWO, "Nonsense, maybe if One started us off you’ll get into it. Let’s try it, "
                                        "just for a little bit.")
        slow_type(85, Bcolors.CORE_TWO, "Okay, fine, I’ll start. Type an adjective ending in -ing to calibrate our "
                                        "system, and make sure the word describes 2020 for you.")
        ONE_WORD = input()


introduction()
# print(NAME)
# stats = Stats()
# stats.print_stats()
# # INTRODUCTION
#
# x = input()
# print('hello world')
#
# print('Hello, ' + x)
#
# events = {'Money': ['Lots of money', 'No money'], 'Money2': ['Lots of money', 'No money'],
#           'Money3': ['Lots of money', 'No money']}
# sequential_words = ['first', 'next', 'third', 'following', 'next', 'fifth']  # Add as many as needed here
# keys = list(events.keys())
# print(keys)
# random.shuffle(keys)
# print(keys)
#
# for i in range(len(keys)):
#     if keys[i] is "Money":
#         c = 0
#     # r = random.randint(0, 1)
#     # print(events.get(keys[i])[r])
