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
    wealth = '→'  # ↑ → or ↓ to signify relative money movement
    stress = 0
    days_quarantined = 0
    fields = [50, 50, '→', 0, 0]
    flags = [0, 0, 0, 0, 0]
    stat_message = ['Happiness: ', '\tMental Health: ', '\tWealth: ', '\tStress: ', '\tDays Quarantined: ']

    def print_stats(self):
        for i in range(len(self.flags)):
            if self.flags[i] == -1:
                print(Bcolors.FAIL + self.stat_message[i] + str(self.fields[i]) + Bcolors.ENDC, end='')
            elif self.flags[i] == 0:
                print(Bcolors.CORE_ONE + self.stat_message[i] + str(self.fields[i]) + Bcolors.ENDC, end='')
            else:  # 1 case
                print(Bcolors.OKGREEN + self.stat_message[i] + str(self.fields[i]) + Bcolors.ENDC, end='')
        print('\n')
        # print(Bcolors.FAIL + 'Happiness: ' + str(self.happiness) + ' | Mental Health: ' + str(self.mental_wellbeing)
        #       + Bcolors.ENDC)
        self.flags = [0, 0, 0, 0, 0]

    def set_happiness(self, new):
        if self.happiness + new < 0:
            val = round(self.happiness / 2)
        elif self.happiness + new > 100:
            val = round(((100 - self.happiness)/2) + self.happiness)
        else:
            val = self.happiness + new
        if val < self.happiness:
            self.flags[0] = -1
        elif val == self.happiness:
            self.flags[0] = 0
        else:
            self.flags[0] = 1
        self.happiness = val
        self.fields[0] = val

    def set_mental(self, new):
        if self.mental_wellbeing + new < 0:
            val = round(self.mental_wellbeing / 2)
        elif self.mental_wellbeing + new > 100:
            val = round(((100 - self.mental_wellbeing)/2) + self.mental_wellbeing)
        else:
            val = self.mental_wellbeing + new
        if val < self.mental_wellbeing:
            self.flags[1] = -1
        elif val == self.mental_wellbeing:
            self.flags[1] = 0
        else:
            self.flags[1] = 1
        self.mental_wellbeing = val
        self.fields[1] = val

    def set_wealth(self, new):
        if new == 'up':
            val = '↑'
        elif new == 'down':
            val = '↓'
        elif new == 'upup':
            val = '↑↑'
        elif new == 'downdown':
            val = '↓↓'
        else:
            val = '→'

        if val < self.wealth:
            self.flags[2] = -1
        elif val == self.wealth:
            self.flags[2] = 0
        else:
            self.flags[2] = 1

        self.wealth = val
        self.fields[2] = val

    def set_stress(self, new):
        if self.stress + new < 0:
            val = round(self.stress / 2)
        elif self.stress + new > 100:
            val = round(((100 - self.stress)/2) + self.stress)
        else:
            val = self.stress + new

        if val < self.stress:
            self.flags[3] = 1
        elif val == self.stress:
            self.flags[3] = 0
        else:
            self.flags[3] = -1

        self.stress = val
        self.fields[3] = val

    def set_days_quarantined(self, new):
        if self.days_quarantined + new < 0:
            val = round(self.days_quarantined / 2)
        elif self.days_quarantined + new > 100:
            val = round(((100 - self.days_quarantined)/2) + self.days_quarantined)
        else:
            val = self.days_quarantined + new

        if val < self.days_quarantined:
            self.flags[4] = 1
        elif val == self.days_quarantined:
            self.flags[4] = 0
        else:
            self.flags[4] = -1

        self.stress = val
        self.fields[4] = val

    def set_all(self, lst):
        self.set_happiness(lst[0])
        self.set_mental(lst[1])
        self.set_wealth(lst[2])
        self.set_stress(lst[3])
        self.set_days_quarantined(lst[4])


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


# Event list with all the scenarios and impact to stats
events = {'School': [(' You sit down at a spotless, spacious desk and log on to a zoom call from your private room. '
                    'Wifi is never an issue and you tons of screen real estate to work with.', [0, 0, 'even', -20, 5]),
                     ('The wifi doesn’t reach your room, so you trudge out to the kitchen where your family is '
                      'arguing about something. Sit down, log in and watch the lecture on your cracked laptop screen, trying to tune out the background noise.', [-20, -10, 'even', 25, 5])]}


keys = list(events.keys())
print(keys)
random.shuffle(keys)
print(keys)


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


# introduction()
# print(NAME)

# stats = Stats()
# stats.print_stats()
# stats.set_happiness(25)
# stats.print_stats()
# print(stats.fields)



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
#
for i in range(len(keys)):
    # if keys[i] is "Money":
    #     c = 0
    r = random.randint(0, len(events.get(keys[i])) - 1)
    stats.set_all(events.get(keys[i])[r][1])
    stats.print_stats()
    # print(events.get(keys[i])[r])
