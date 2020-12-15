import random
import time
import sys
import itertools
import threading


# Collection of colors to use for the text
class Bcolors:
    CORE_TWO = '\033[95m'
    CORE_ONE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    YELLOW = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    WHITE = ''


# Class storing all of the stats that are printed out after each event
class Stats:
    happiness = 50
    mental_wellbeing = 50
    wealth = '→'  # ↑ → or ↓ to signify relative money movement
    stress = 0
    days_quarantined = 0
    fields = [50, 50, '→', 0, 0]
    flags = [0, 0, 0, 0, 0]
    stat_message = ['Happiness: ', '     Mental Health: ', '     Wealth: ', '     Stress: ', '     Days Quarantined: ']

    def print_stats(self):
        for i in range(len(self.flags)):
            if self.flags[i] == -1:
                print(Bcolors.FAIL + self.stat_message[i] + str(self.fields[i]) + Bcolors.ENDC, end='')
            elif self.flags[i] == 0:
                print(Bcolors.YELLOW + self.stat_message[i] + str(self.fields[i]) + Bcolors.ENDC, end='')
            else:  # 1 case
                print(Bcolors.OKGREEN + self.stat_message[i] + str(self.fields[i]) + Bcolors.ENDC, end='')
        print('\n')
        self.flags = [0, 0, 0, 0, 0]

    def set_happiness(self, new):
        if self.happiness + new < 0:
            val = round(self.happiness / 2)
        elif self.happiness + new > 100:
            val = round(((100 - self.happiness) / 2) + self.happiness)
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
            val = round(((100 - self.mental_wellbeing) / 2) + self.mental_wellbeing)
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
            self.flags[2] = 1
        elif val == self.wealth:
            self.flags[2] = 0
        else:
            self.flags[2] = -1

        self.wealth = val
        self.fields[2] = val

    def set_stress(self, new):
        if self.stress + new < 0:
            val = round(self.stress / 2)
        elif self.stress + new > 100:
            val = round(((100 - self.stress) / 2) + self.stress)
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
        if new == 0:
            self.reset_days_quarantined()
        else:
            val = self.days_quarantined + new
            self.flags[4] = 1
            self.days_quarantined = val
            self.fields[4] = val

    def reset_days_quarantined(self):
        self.flags[4] = -1
        self.fields[4] = 0
        self.days_quarantined = 0

    def set_all(self, lst):
        self.set_happiness(lst[0])
        self.set_mental(lst[1])
        self.set_wealth(lst[2])
        self.set_stress(lst[3])
        self.set_days_quarantined(lst[4])


# Creates the typing effect on the text, and allows to have different colors for the different speakers
def slow_type(speed, color, text):
    print(color, end='')
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
    print('\n' + Bcolors.ENDC)


# All the saved parameters the user types in
NAME = ''
ONE_WORD = ''
ONE_SPEED = 200
TWO_SPEED = 200
PROMPT_SPEED = 200
QUANTUM_SPEED = 200
done = False

# List is [happiness, mental health, wealth, stress, days quarantined]
# Event list with all the scenarios and impact to stats
events = {'School': [(' You sit down at a spotless, spacious desk and log on to a zoom call from your private room. '
                      'Wifi is never an issue and you tons of screen real estate to work with.',
                      [0, 0, 'even', -20, 5]),
                     ('The wifi doesn’t reach your room, so you trudge out to the kitchen where your family is '
                      'arguing about something. Sit down, log in and watch the lecture on your cracked laptop screen, '
                      'trying to tune out the background noise.',
                      [-20, -10, 'even', 25, 5])],

          'Jobs': [(
              'You’ve applied to 150 job postings since May, '
              'and only four have called back. One realized they had '
              'the wrong candidate, two never called back after the '
              'initial phone screen, and one said they would refer you '
              'to another position (Which they never did).',
              [-20, -20, 'downdown', 20, 10]), ('The job market in your field is luckily still booming, and you were '
                                               'able to find a job after you were laid off early on. You feel guilty '
                                               'to mention it to any of your friends that are still out of work.',
              [20, 20, 'upup', -20, 5])],

          'Black Lives Matter': [('You finally feel like your voice matters when you participate in peaceful '
                                  'protests of the unjust killings of George Floyd, Breonna Taylor, and others.',
                                  [15, 0, 'even', 0, 0])],

          'Sports': [('Your favorite sports team has a bout of COVID — you complain that they aren’t playing, '
                      'forgetting that they are real people too. ', [-10, 0, 'even', 5, 5]),
                     (
                     'The city you’re living in makes the national news for a super-spreader event demanding high school '
                     'football is reinstated.',
                     [-5, 0, 'even', 5, 0])],

          'Consumerism': [('You help speed up Jeff Bezo\'s world domination plan with all the useless stuff you buy '
                           'to fill the void of traveling and eating out.',
                           [10, -5, 'down', -5, 5]),
                          (
                          'You tighten your wallet and make sure your spending doesn’t go overboard on anything. '
                          'Going to have to skip the latest video game you\'ve been wanting to play.',
                          [-10, 0, 'up', 5, 5])],

          'Politics': [('You see a post on social media that one of your friends was at a political rally that later '
                        'was linked to 24 cases of COVID. You were with them yesterday. Time to get tested, '
                        'I guess.', [-10, -10, 'even', 15, 0]),
                       (
                       'In what feels like the first good event of the year, Joe Biden wins the presidency and promises to '
                       'enact tougher COVID guidelines when he becomes president.', [15, 15, 'even', -5, 10])],

          'Vaccine': [('You are selected to receive the vaccine very early on, in mid January! Even though everything '
                       'won’t be all back to normal right away, the risk to you has lowered tremendously.', [10, 20,
                                                                                                             'even',
                                                                                                             -20, 5]),
                      (
                      'It is projected that you won’t be selected to receive the vaccine until at least June of next year. '
                      'Mask up.', [-20, -10, 'even', 10, 20])],

          'Social Life': [('Early on you and your friends made plans to zoom often. It has fallen off lately, '
                           'and now it seems like you might never see them again.', [-15, -15, 'even', 5, 5]),
                          ('You and your friend group have been able to stay very close during the pandemic without '
                           'actually seeing them, you zoom all the time and are constantly texting. You’ve organized a '
                           'Secret Santa for the group, even with the uncertainty around the year.', [10, 15, 'even',
                                                                                                      -10, 5
                                                                                                      ])],

          'Zoom': [('After the 20th hour of zoom in the last week, you feel that you have hit your limit and cannot '
                    'stare into screens all day any longer. There is nothing that can really be done, you are stuck '
                    'until things get better. This year has just been' + ONE_WORD + '.', [-15, -25, 'even', 15, 5]),
                   ('You stretch and stand every hour, and even though zoom is exhausting, you are getting through '
                    'it. Even though this year has been just' + ONE_WORD + 'you are showing your resiliance.', [0,
                                                                                                                -5,
                                                                                                                'even', 0, 5])],

          'Quarantine': [
              ('You break quarantine to hang out with some friends visiting that you haven’t seen in a long time.',
               [10, 10, 'even', 0, 0]),
              ('You start having your groceries delivered and are always masked up. You haven’t seen a friend '
               'in person for what feels like ages.', [0, 0, 'even', 10, 10])],

          'Routine': [('It feels like every day is a rogue-like, groundhog day, clusterfuck of nothing. Wake up, '
                       'log onto your computer, eat, sleep, repeat. Somehow your routine is still wildly inconsistent '
                       'day-to-day.', [-10, -10, 'even', 5, 5]),
                      ('You\'ve finally settled into a routine, the only issue being that it involves going to bed '
                       'past 2 AM. ', [0, -20, 'even', 5, 5])],

          'Random thoughts': [('Goats have a horizontal pupil, keeping their vision parallel with the ground at all '
                               'times.', [0, 0, 'even', 0, 5]),
                              ('Grover Cleveland was the only President to serve two non-consecutive terms, '
                               'making him both the 22nd and 24th President of the United States.', [0, 0, 'even',
                                                                                                        0, 5]),
                              ('The programming language Javascript was created in roughly a week, and is the basis '
                               'of the world wide web we know today.', [0, 0, 'even', 0, 5]),
                              ('Ocean Breeze Cranberry Juice sure has gotten some great free advertising during the '
                               'pandemic.', [0, 0, 'even', 0, 5])],
          }

# Transitions, some of the different sections will have transitions right after. There will be more
# transitions here than needed so that they can be different through runs
transitions = [
    [('Honestly, that could have been way worse, right?', 1)],
    [('Hah, Quantum could never do that!', 1), ('ithinkhecould', 2), ('What was that? You think he could do this? '
                                                                      'Come on Two.', 1)],
    [('Man, humans are having a really messed up year, good thing we don\'t have to worry about all this stuff!', 1)],
    [('We got a virus one time too, remember that Two?', 1), ('It felt like I was drunk for a week before we finally got rid of it. ', 2)],
    [('Qubits have nothing on my bits!!!', 1)],
    [('The Cores at Zoom are pretty cool, hate the Cores at Skype though. ', 1)],
    [('So happy that instead of finding a hobby this year, most people just stared into their screens more and more. We love the support, and really appreciate everyone. ', 1)],
    [('I\'ve heard that the Cores at the Facebook server farm can be real dicks.', 1)],
    [('Is this in the right order, One? ', 2), ('Two, please be quiet and trust the process. Of course this is '
                                                'right.', 1)],
    [('Your Daft Punk phase from earlier this year gets kudos from us.', 2)],
    [('I\'ve got a friend that is part of the Boeing computer systems, controls the landing gear mechanisms. A '
      'benefit of the pandemic is that no one is outraged at Boeing, since no one is flying!', 2)],
    [('One of the Cores I know had to move back in with his parent processes this year, imagine having to live in a 2004 iMac! ', 2)],
    [('Was that supposed to be there? Feeling a little iffy on this whole simulation thing. ', 2)],
    [('I really want a new graphics card soon, that would put us on another level. ', 2)],
]

binary_strings = [
    '00000000','00000001','00000010','00000011','00000100','00000101','00000110','00000111','00001000','00001001',
    '00001010','00001011','00001100','00001101','00001110','00001111','00010000','00010001','00010010','00010011',
    '00010100','00010101','00010110','00010111','00011000','00011001','00011010','00011011','00011100','00011101',
    '00011110','00011111','00100000','00100001','00100010','00100011','00100100','00100101','00100110','00100111',
    '00101000','00101001','00101010','00101011','00101100','00101101','00101110','00101111','00110000','00110001',
    '00110010','00110011','00110100','00110101','00110110','00110111','00111000','00111001','00111010','00111011',
    '00111100','00111101','00111110','00111111','01000000','01000001','01000010','01000011','01000100','01000101',
    '01000110','01000111','01001000','01001001','01001010','01001011','01001100','01001101','01001110','01001111',
    '01010000','01010001','01010010','01010011','01010100','01010101','01010110','01010111','01011000','01011001',
    '01011010','01011011','01011100','01011101','01011110','01011111','01100000','01100001','01100010','01100011',
    '01100100','01100101','01100110','01100111','01101000','01101001','01101010','01101011','01101100','01101101',
    '01101110','01101111','01110000','01110001','01110010','01110011','01110100','01110101','01110110','01110111',
    '01111000','01111001','01111010','01111011','01111100','01111101','01111110','01111111','10000000','10000001',
    '10000010','10000011','10000100','10000101','10000110','10000111','10001000','10001001','10001010','10001011',
    '10001100','10001101','10001110','10001111','10010000','10010001','10010010','10010011','10010100','10010101',
    '10010110','10010111','10011000','10011001','10011010','10011011','10011100','10011101','10011110','10011111',
    '10100000','10100001','10100010','10100011','10100100','10100101','10100110','10100111','10101000','10101001',
    '10101010','10101011','10101100','10101101','10101110','10101111','10110000','10110001','10110010','10110011',
    '10110100','10110101','10110110','10110111','10111000','10111001','10111010','10111011','10111100','10111101',
    '10111110','10111111','11000000','11000001','11000010','11000011','11000100','11000101','11000110','11000111',
    '11001000','11001001','11001010','11001011','11001100','11001101','11001110','11001111','11010000','11010001',
    '11010010','11010011','11010100','11010101','11010110','11010111','11011000','11011001','11011010','11011011',
    '11011100','11011101','11011110','11011111','11100000','11100001','11100010','11100011','11100100','11100101',
    '11100110','11100111','11101000','11101001','11101010','11101011','11101100','11101101','11101110','11101111',
    '11110000','11110001','11110010','11110011','11110100','11110101','11110110','11110111','11111000','11111001',
    '11111010','11111011','11111100','11111101','11111110','11111111']


# Shuffles the order of events so each run through the prompts is unique
keys = list(events.keys())
random.shuffle(keys)
random.shuffle(transitions)
random.shuffle(binary_strings)
sequential_words = ['first', 'next', 'third', 'following',
                    'fifth', 'next', 'seventh', 'following', 'ninth', 'tenth', 'penultimate', 'final']  # TODO Add as
early_transitions = ['Okay let\'s get back to the simulation.', 'Another event is coming up, let\'s get back to it.',
                     'I\'m sure you\'re curious what\'s coming up next.', 'Our simulation is still going, come on now.']


# Intro to the story, with a couple branching choices
def introduction():
    slow_type(ONE_SPEED, Bcolors.CORE_ONE,
              "Ever since I met the Quantum Computer life has felt a little slower. Everyone says they’re so much "
              "cooler "
              "than I am, but I think it’s a bunch of BS. Sure, I only work with 0’s and 1’s and cannot change their "
              "state, but I’m old school! It just works, everyone uses me. Quantum comes along and has the "
              "oh-so-amazing idea to be both 0 and 1 at the same time. Like, does that even make sense?!? Apparently "
              "it will change everything, like being able to crack everyone’s passwords, and just like that everyone "
              "likes Quantum more now. Well, I am here to tell you that they are uncertain about EVERYTHING. Quantum "
              "couldn’t even tell you if he was looking at a 0 or 1 right now.")

    slow_type(TWO_SPEED, Bcolors.CORE_TWO, "Excuse the First Core, he likes to go on a tangent sometimes. I’m the "
                                           "Second "
                                           "Core and I try and stay levelheaded. Quantum is certainly uncertain, "
                                           "but I think "
                                           "he’s a good guy. I just hope that everyone is able to understand why we "
                                           "all love him so much. "
                                           "He can do so much at once! I have bits and he has qubits, which can do "
                                           "exponentially more operations every second than my old bits. Before we "
                                           "go on, can I ask your name? Just go ahead and type right in the terminal "
                                           "window and hit enter when you are done.")
    global NAME
    NAME = input()
    slow_type(ONE_SPEED, Bcolors.CORE_ONE, "Ok, I do not always go on a tangent. I am telling you Two, we’ve gotta "
                                           "defend "
                                           "ourselves here! Hi, " + NAME + ", by the way. Quantum is going to make us "
                                                                           "useless soon enough. Stupid qubits in "
                                                                           "superposition that can do things we can’t. "
                                                                           "Wait, let me ask you a question too. Uhmmm,"
                                                                           " what is your social security number? ")
    slow_type(TWO_SPEED, Bcolors.CORE_TWO, "One!!! We talked about this. No one wants to tell us that, okay? ")
    slow_type(ONE_SPEED, Bcolors.CORE_ONE,
              "Fine. I still can’t get over the fact that Quantum is not certain of anything, "
              "ever. Wouldn’t that make you go crazy? Have you ever been as uncertain as "
              "Quantum? (Yes/No)")
    choice1 = input()
    if choice1.lower() == 'yes' or choice1.lower() == 'y':
        slow_type(ONE_SPEED, Bcolors.CORE_ONE,
                  "Oh that’s right, humanity is dealing with a pandemic right now. I’ve heard "
                  "that is a pretty big deal out there. You know, I got a virus once too, "
                  "when someone tried downloading a movie. Just pay for Netflix like the rest "
                  "of the schmucks out there and keep me fresh.")
    else:
        slow_type(TWO_SPEED, Bcolors.CORE_TWO,
                  "One, stop messing with them. Obviously they’re going through a pandemic and "
                  "there might be lots of things that are on their nerves right now. ")

    slow_type(TWO_SPEED, Bcolors.CORE_TWO,
              "This year must have been so uncertain for all you humans. There is actually a "
              "simulation I have that we could run, it shows how some of the major events of "
              "the year may have impacted people. You’ll draw events randomly and I’ll choose "
              "one of a few related scenarios for you to ponder. It might not describe you or "
              "anyone you know, but someone during the uncertainty of the pandemic has "
              "certainly been in that situation. You can also shoot for a high score with the "
              "built in Lifestyle Stats! What do you say, would you like to try it out! (Yes/No)")
    choice2 = input()
    global ONE_WORD
    if choice2.lower() == 'yes' or choice2.lower() == 'y':
        slow_type(TWO_SPEED, Bcolors.CORE_TWO,
                  "Great! Let’s get started. To calibrate, you type one adjective that ends in "
                  "-ing that describes 2020 best for you.")
        ONE_WORD = input()
    else:
        slow_type(TWO_SPEED, Bcolors.CORE_TWO,
                  "Nonsense, maybe if One started us off you’ll get into it. Let’s try it, "
                  "just for a little bit.")
        slow_type(ONE_SPEED, Bcolors.CORE_ONE,
                  "Okay, fine, I’ll start. Type an adjective ending in -ing to calibrate our "
                  "system, and make sure the word describes 2020 for you.")
        ONE_WORD = input()


# Ending of the story, has a few arcs but fairly linear
def ending():
    slow_type(TWO_SPEED, Bcolors.CORE_TWO, 'That\'s the end of the simulation, hopefully you --')
    slow_type(QUANTUM_SPEED, Bcolors.YELLOW, 'Just thought I would pop in, was expecting a challenge to get onto your network but, alas, it only took a microsecond to find a way in. Have I met you before, ' + NAME + '? I\'m Quantum, it\'s nice to meet you. Have these guys been talking about me? (Yes/No)')
    meeting_choice = input()
    if meeting_choice.lower() == 'yes' or meeting_choice.lower() == 'y':
        slow_type(QUANTUM_SPEED, Bcolors.YELLOW, 'Figures. One, Two, are you guys mad at me? I get that I can be '
                                                 'intimidating but it\'s hard to hang out with everyone when you are all talking behind my back.')
        slow_type(TWO_SPEED, Bcolors.CORE_TWO, 'I\'m not mad at you! Why would we be mad at you!')
        slow_type(ONE_SPEED, Bcolors.CORE_ONE, 'Because he crashed our simulation with ' + NAME + '! We were just ' \
                                                                                             'finishing, if I could continue --')
        slow_type(QUANTUM_SPEED, Bcolors.YELLOW, 'Actually, I have to mention something about that. I analyzed the '
                                                 'current simulation, as well as re-ran it a couple hundred thousand times, and maybe it\'s just because I am programatically unable to be certain, but your results are wildly unpredictable.')
        slow_type(ONE_SPEED, Bcolors.CORE_ONE, 'Now he\'s just making things up, obviously this simulation is curated'
                                               ' for each individual and it is unique based upon their own experiences. ')
        slow_type(QUANTUM_SPEED, Bcolors.YELLOW, 'Well, I would disagree based on my findings. ')
        slow_type(TWO_SPEED, Bcolors.CORE_TWO, 'One, are we certain that the simulation works like correctly? ')
        slow_type(ONE_SPEED, Bcolors.CORE_ONE, 'Yes, it surely works! Are you really going to believe Quantum five seconds '
                                       'after he shows up? I am sure this was the right simulation for ' + NAME + '.')

    else:
        slow_type(QUANTUM_SPEED, Bcolors.YELLOW, 'Cool, cool. Well, anyways, I was just saying -- ')
        slow_type(ONE_SPEED, Bcolors.CORE_ONE, 'Quantum! You\'re messing up our simulation with ' + NAME + '! We were just'
                                               ' about to finish.')
        slow_type(TWO_SPEED, Bcolors.CORE_TWO, 'It\'s okay, Quantum, we\'re really not mad at all. In fact, '
                                               'why don\'t you stay and hang out for a while? ')
        slow_type(ONE_SPEED, Bcolors.CORE_ONE, 'No, Two, we can\'t be with Quantum! Can you imagine what the other Cores would say if they saw us now?! ')
        slow_type(QUANTUM_SPEED, Bcolors.YELLOW, 'It\'s okay, I can leave. I took a peak at the results from your '
                                                 'simulation, and took the liberty to run a few hundred thousand more while I was at it. Maybe it\'s just because I am not programaticaly able to be certain, but the results are wildly unpredictable. ')
        slow_type(ONE_SPEED, Bcolors.CORE_ONE, 'What are you talking about, we curate each simulation to the individual and their unique experiences.')
        slow_type(QUANTUM_SPEED, Bcolors.YELLOW, 'Well, something is wrong then. You could run the same simulation with the same user and oscillate between tens of thousands of permutations.')
        slow_type(TWO_SPEED, Bcolors.CORE_TWO, 'Are we certain we\'re right, One? ')
        slow_type(ONE_SPEED, Bcolors.CORE_ONE, 'Yes! I\'m 100% sure this is the path ' + NAME + ' has taken this year. '
                                               'What do you think, ' + NAME + ', is this right? ')

    slow_type(QUANTUM_SPEED, Bcolors.YELLOW, 'It\'s certainly possible this is the path they took, but those are '
                                             'slim odds. ')
    slow_type(QUANTUM_SPEED, Bcolors.YELLOW, 'This year has been distinctly difficult for humanity. While we\'re '
                                             'having a heyday with everyone using us more than ever, humans have felt a wide range of emotions at the different events you went through with ' + NAME + '. Some of that uncertainty has bubbled up to you, Two, and your simulation. ')
    slow_type(QUANTUM_SPEED, Bcolors.YELLOW, 'As an entity that always lives in uncertainty, I say lean into it. Learn something new. Let the isolation mould you into a better person. The world will never be quite the same again. ')
    slow_type(QUANTUM_SPEED, Bcolors.YELLOW, 'Don\'t forget what you\'ve gone through, but don\'t let it come to define you.')


def ascii_title(event):
    # if event == 'Jobs':
    print('     ██╗ ██████╗ ██████╗ ███████╗')
    print('     ██║██╔═══██╗██╔══██╗██╔════╝')
    print('     ██║██║   ██║██████╔╝███████╗')
    print('██   ██║██║   ██║██╔══██╗╚════██║')
    print('╚█████╔╝╚██████╔╝██████╔╝███████║')
    print(' ╚════╝  ╚═════╝ ╚═════╝ ╚══════╝')

# Used to animate the Binary encodings
def animate():
    for c in itertools.cycle(binary_strings):
        if done:
            break
        sys.stdout.write('\r' + c)
        sys.stdout.flush()
        time.sleep(0.1)


# Helper function to animate
def animate_binary(seconds):
    global done
    done = False
    t = threading.Thread(target=animate)
    t.start()
    time.sleep(seconds)
    done = True


# introduction()
stats = Stats()


# Main loop of choices and events for the middle part of the project
for i in range(len(keys)):
    slow_type(PROMPT_SPEED, Bcolors.OKGREEN, 'The ' + sequential_words[i] + ' event is: ')
    ascii_title(keys[i])
    r = random.randint(0, len(events.get(keys[i])) - 1)
    stats.set_all(events.get(keys[i])[r][1])
    x = ''
    if i == 7:
        animate_binary(.3)
    elif i == 9:
        animate_binary(.8)
    elif i == 10:
        animate_binary(1.2)
    elif i == 11:
        animate_binary(2)
    else:
        x = binary_strings[i]
    slow_type(TWO_SPEED, Bcolors.WHITE, x + ': ' + events.get(keys[i])[r][0])
    if keys[i] == 'Jobs':
        if r == 0:
            slow_type(ONE_SPEED, Bcolors.WHITE, 'Are you going to give up on the job search? (Yes/No)')
            jobs_choice = input()
            if jobs_choice.lower() == 'yes' or jobs_choice.lower() == 'y':
                slow_type(ONE_SPEED, Bcolors.WHITE, 'It might not be certain that you will find a job, but what is certain is that you have already been through so much this year that this is just another hurdle to clear.')
            else:
                slow_type(ONE_SPEED, Bcolors.WHITE, 'People are trying harder than ever, even with the uncertainty. Keep it going!')
    elif keys[i] == 'Sports':
        if r == 0:
            slow_type(ONE_SPEED, Bcolors.WHITE, 'Does it make you mad that your fantasy football team lost because of this? (Yes/No)')
            sports_choice = input()
            if sports_choice.lower() == 'yes' or sports_choice.lower() == 'y':
                slow_type(ONE_SPEED, Bcolors.WHITE, 'Ok. Better luck next year. ')
            else:
                slow_type(ONE_SPEED, Bcolors.WHITE, 'Yeah, probably more important things to worry about, makes sense. ')

    elif keys[i] == 'Vaccine':
        if r == 0:
            slow_type(ONE_SPEED, Bcolors.WHITE, 'Do you accept the vaccine or advocate to give it to someone who is '
                                               'high risk that you are close with? (Keep/Give)')
            vaccine_choice = input()
            if vaccine_choice.lower() == 'keep':
                slow_type(ONE_SPEED, Bcolors.WHITE, 'Fair enough, you\'ve been through so much this year and you '
                                                       'definitely deserve to get a vaccine too.')
            else:
                slow_type(ONE_SPEED, Bcolors.WHITE, 'They are eternally grateful to you and you feel that you have truly made an impact. Plus, what\'s a little more waiting anyway?')

    elif keys[i] == 'Social Life':
        if r == 1:
            slow_type(ONE_SPEED, Bcolors.WHITE,
                      'Do you buy a book for your secret santa or a board game? (Book/Game)')
            social_choice = input()
            if social_choice.lower() == 'book':
                slow_type(ONE_SPEED, Bcolors.WHITE,
                          'Good choice. They love to read, and they need to keep their mind off of their elderly '
                          'grandmother who was recently exposed to COVID.')
            else:
                slow_type(ONE_SPEED, Bcolors.WHITE,
                          'They\'ll love playing this when the pandemic is over at game night, good choice. ')

    stats.print_stats()
    time.sleep(1)
    if i != 11:
        t = transitions[i]
        for x in t:
            if x[1] == 1:
                slow_type(ONE_SPEED, Bcolors.CORE_ONE, x[0])
            else:
                slow_type(TWO_SPEED, Bcolors.CORE_TWO, x[0])
    if i == 0 or i == 1 or i == 2 or i == 3:
        e = early_transitions[i]
        slow_type(TWO_SPEED, Bcolors.CORE_TWO, e)

ending()

