import time
import random 
import io

class key:
    def key(self):
        return "10jifn2eonvgp1o2ornfdlf-1230"

class ai:
    def __init__(self):
        pass

    class state:
        def __init__(self, a, b, a_fin, b_fin):
            self.a = a
            self.b = b
            self.a_fin = a_fin
            self.b_fin = b_fin

    # Kalah:
    #         b[5]  b[4]  b[3]  b[2]  b[1]  b[0]
    # b_fin                                         a_fin
    #         a[0]  a[1]  a[2]  a[3]  a[4]  a[5]
    # Main function call:
    # Input:
    # a: a[5] array storing the stones in your holes
    # b: b[5] array storing the stones in opponent's holes
    # a_fin: Your scoring hole (Kalah)
    # b_fin: Opponent's scoring hole (Kalah)
    # t: search time limit (ms)
    # a always moves first
    #
    # Return:
    # You should return a value 0-5 number indicating your move, with search time limitation given as parameter
    # If you are eligible for a second move, just neglect. The framework will call this function again
    # You need to design your heuristics.
    # You must use minimax search with alpha-beta pruning as the basic algorithm
    # use timer to limit search, for example:
    # start = time.time()
    # end = time.time()
    # elapsed_time = end - start
    # if elapsed_time * 1000 >= t:
    #    return result immediately 
    def move(self, a, b, a_fin, b_fin, t):
        #For test only: return a random move
        #r = []
        #for i in range(6):
        #    if a[i] != 0:
        #        r.append(i)
        # To test the execution time, use time and file modules
        # In your experiments, you can try different depth, for example:
        #f = open('time.txt', 'a') #append to time.txt so that you can see running time for all moves.
        # Make sure to clean the file before each of your experiment
        #for d in [3, 5, 7]: #You should try more
        #    f.write('depth = '+str(d)+'\n')
        #    t_start = time.time()
        #    self.minimax(depth = d)
        #    f.write(str(time.time()-t_start)+'\n')
        #f.close()
        #return r[random.randint(0, len(r)-1)]
        #But remember in your final version you should choose only one depth according to your CPU speed (TA's is 3.4GHz)
        #and remove timing code. 
        
        #Comment all the code above and start your code here
        currstate = self.state(a,b,a_fin,b_fin) # create the initial game state
        currmove = self.minimax(5, currstate) # call minimax search and then return the best move
        return currmove
    
    global max
    max = float('inf')
    global min
    min = float('-inf')

    # generating the max state with the alpha beta pruning 
    def generateMaxStates(self, state, beta, depth):
        temp = min
        curr = 0
        if depth==0: # terminal state
            return None, self.heuristics(state)
        for i in range(6): # generate the successors for the possible moves
            if state.a[i] != 0:
                cagain, new_state = self.next(state, i, 'user')
                if cagain == True:
                    a, b = self.generateMaxStates(new_state, max, depth-1)
                else:
                    a, b = self.generateMinStates(new_state, temp, depth-1) 
                if b > temp:  
                    temp = b
                    curr = i
        return curr, temp # return the index and the val of the best move

    # generating min state with alpha beta pruning
    def generateMinStates(self, state, alpha, depth):
        temp = max
        curr = 0
        if depth==0: # terminal state
            return None, self.heuristics(state)
        for i in range(6):
            if state.a[i] != 0:
                cagain, new_state = self.next(state, i, 'ai')
                if cagain == True:
                    a, b = self.generateMinStates(new_state, min, depth-1)
                else:
                    a, b = self.generateMaxStates(new_state, temp, depth-1)
                if b < temp:
                    temp = b
                    curr = i
        return curr, temp         

    # heuristic function that takes into account the difference in total and
    # also weighs in having more stones on your side of the board
    def heuristics(self, state): 
        playersum = sum(state.a)
        oppsum = sum(state.b)
        return (state.a_fin - state.b_fin) + ((playersum - oppsum) / 5)

    # reusing the updatelocalstate() function from main.py to generate the successor states 
    # checks if it's the ai or the opponents turn, and flips the values accordingly
    # returns the newstate generated along with a boolean value
    def next(self, state, move, user):
        if user == 'ai':
            a = state.b
            b = state.a
            a_fin = state.b_fin
            b_fin = state.a_fin
        else:
            a = state.a
            b = state.b
            a_fin = state.a_fin
            b_fin = state.b_fin
        ao = a[:]
        all = a[move:] + [a_fin] + b + a[:move]
        count = a[move]
        all[0] = 0
        p = 1
        while count > 0:
            all[p] += 1
            p = (p + 1) % 13
            count -= 1
        a_fin = all[6 - move]
        b = all[7 - move:13 - move]
        a = all[13 - move:] + all[:6-move]
        cagain = bool()
        ceat = False
        p = (p - 1) % 13
        if p == 6 - move:
            cagain = True
        if p <= 5 - move and ao[move] < 14:
            id = p + move
            if (ao[id] == 0 or p % 13 == 0) and b[5 - id] > 0:
                ceat = True
        elif p >= 13 - move and ao[move] < 14:
            id = p + move - 13
            if (ao[id] == 0 or p % 13 == 0) and b[5 - id] > 0:
                ceat = True
        if ceat:
            a_fin += b[5-id]+1
            b[5-id] = 0
            a[id] = 0
        if sum(a)==0:
            b_fin += sum(b)
        if sum(b)==0:
            a_fin += sum(a)
        if user == 'ai':
            new_state = self.state(b,a, b_fin, a_fin)
        else:
            new_state = self.state(a, b, a_fin, b_fin)
        return cagain, new_state

    # calling function to generate the states using the minimax search
    def minimax(self, depth, state):
        currmove, temp = self.generateMaxStates(state, max, depth)
        return currmove
    
