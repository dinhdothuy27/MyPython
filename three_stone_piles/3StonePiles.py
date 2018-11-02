# Rule: 2 players will play with 3 stone piles. Each stone pile has n<=100 stones
# In player A's turn, A can get k>0 stones in one of 3 stone piles.
# 2 players will get stones until 3 stone piles is clear
# Finally, winner is who play last turn

import numpy as np
import pickle
import random
import os.path

ALPHA = 0.1
EPSILON = 0.1
NUMOFSTONES = 100

end_state = (0,0,0)
estimations = dict()
for i in range(NUMOFSTONES + 1):
    for j in range(i,NUMOFSTONES + 1):
        for k in range(j,NUMOFSTONES + 1):
            estimations[(i,j,k)] = 0
estimations[end_state] = 1

class State:
    def __init__(self, n1, n2, n3):
        self.SP = (n1,n2,n3)

    def hash(self):
        sp = sorted(self.SP)
        return (sp[0],sp[1],sp[2])

    def is_end(self):
        return not any([(x>0) for x in self.SP])

    def next_state(self, act):
        spi = act[0]
        stones = act[1]
        n =[sp for sp in self.SP]
        if stones>n[spi]: n[spi] = 0
        else: n[spi] -= stones
        return State(n[0], n[1], n[2])

# AI
class Player:
    def __init__(self, epsilon=EPSILON):
        self.epsilon = epsilon
        self.name = "AI"

    # choose an action based on the state
    def act(self, state):
        next_states = []
        actions = []
        for i in range(len(state.SP)):
            for j in range(state.SP[i]):
                actions.append([i, j+1])
                next_states.append(state.next_state(actions[-1]).hash())

        if random.uniform(0,1) < self.epsilon:
            action = random.choice(actions)
            return action

        values = []
        for hash, pos in zip(next_states, actions):
            values.append((estimations[hash], pos))
        np.random.shuffle(values)
        values.sort(key=lambda x: x[0], reverse=True)
        action = values[0][1]
        return action

class HumanPlayer:
    def __init__(self):
        self.name = "You"

    def act(self, state):
        idx = 0
        stones = 0
        while True:
            s = input("Your turn (format: \"stone_pile_index num_of_stones\"): ").split(" ")
            if(len(s)<2):
                print("Wrong format!")
                continue
            try:
                idx = int(s[0])
                stones = int(s[1])
                if idx<3 and stones>0 and stones<=state.SP[idx]:
                    return [idx, stones]
                else: print("Wrong input value!")
            except ValueError:
                print("Wrong format!")

def train(epochs):
    player = Player(epsilon=0.01)
    for count in range(epochs):
        states = [[],[]]
        lastP = 0
        a = random.randint(0,NUMOFSTONES)
        b = random.randint(a,NUMOFSTONES)
        c = random.randint(b, NUMOFSTONES)
        curSate = State(a,b,c)

        while True:
            if curSate.is_end():
                states[lastP].append(curSate)
                for j in range(2):
                    sts = [state.hash() for state in states[j]]
                    if len(sts) == 0: continue
                    if not sts[-1] == (0,0,0): estimations[sts[-1]] = -1

                    for i in reversed(range(len(sts) - 1)):
                        state = sts[i]
                        estimations[state] += ALPHA * (estimations[sts[i + 1]] - estimations[state])
                break
            act = player.act(curSate)
            states[lastP].append(curSate)
            curSate = curSate.next_state(act)
            lastP = 1 - lastP

        if count%500 == 499:
            print("train times: {}".format(count+1))

    print("Trainning Done!")

def compete(epochs):
    player = Player(epsilon=0)
    for count in range(epochs):
        states = [[], []]
        lastP = 0
        curSate = State(random.randint(0, NUMOFSTONES), random.randint(0, NUMOFSTONES), random.randint(0, NUMOFSTONES))

        while True:
            if curSate.is_end():
                states[lastP].append(curSate)
                for j in range(2):
                    sts = [state.hash() for state in states[j]]
                    if len(sts) == 0: continue
                    if not sts[-1] == (0, 0, 0): estimations[sts[-1]] = 0

                    for i in reversed(range(len(sts) - 1)):
                        state = sts[i]
                        estimations[state] += ALPHA * (estimations[sts[i + 1]] - estimations[state])
                break
            act = player.act(curSate)
            states[lastP].append(curSate)
            curSate = curSate.next_state(act)
            lastP = 1 - lastP
    print("Compete done!")

def draw_state(state):
    m = max([len(str(st)) for st in state.SP])
    print()
    print("Stone Piles state:")
    print("Stone Pile 0 ({} stones): {}".format(str(state.SP[0]).rjust(m), "* " * state.SP[0]))
    print("Stone Pile 1 ({} stones): {}".format(str(state.SP[1]).rjust(m), "* " * state.SP[1]))
    print("Stone Pile 2 ({} stones): {}".format(str(state.SP[2]).rjust(m), "* " * state.SP[2]))
    print()

# Main
if os.path.isfile("policy.bin"):
    with open('policy.bin', 'rb') as f:
        estimations = pickle.load(f)
if not os.path.isfile("policy.bin") or input("input 1 if you want to train:") == "1":
    train(int(1e4))
    compete(int(1e3))
    with open('policy.bin', 'wb') as f:
        pickle.dump(estimations, f)


print("Let play!")

curSate = State(random.randint(0,NUMOFSTONES),random.randint(0,NUMOFSTONES),random.randint(0,NUMOFSTONES))
draw_state(curSate)

ai = Player(epsilon=0)
human = HumanPlayer()

def alternate():
    while True:
        yield human
        yield ai

alternator = alternate()

while True:
    if curSate.SP == end_state:
        print("{} win!".format(player.name))
        break
    player = next(alternator)
    act = player.act(curSate)
    print("{} take {} stones from Stone Pile {}".format(player.name, act[1], act[0]))
    curSate = curSate.next_state(act)
    draw_state(curSate)

input()
