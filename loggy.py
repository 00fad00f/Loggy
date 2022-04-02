

import numpy as np
import random
import sys
import time


class Board:
    def __init__(self,level):
        '''
        creates attributes for the board class which are the locations of
        the holes and the location of the gloves (both random), the size of the
        board depends on the level
        '''
        hole_pos = []
        glove_pos = []
        if level == 1:
            #4x4 grid
            gameboard = [['*' for x in range(4)] for y in range(4)]
            self.board = np.array(gameboard)
            #generate position of gloves
            while len(glove_pos) < 1:
                gpos = (random.randint(0,3),random.randint(0,3))
                if gpos != (0,0) and gpos != (1,0) and gpos != (0,1):
                    glove_pos.append(gpos)
            #generate list of random hole positions
            while len(hole_pos) < 4:
                pos = (random.randint(1,3),random.randint(1,3))
                #check that this coord isnt where the gloves are or ajacent to loggy start pos
                if pos not in hole_pos and pos not in glove_pos and pos != (0,0) and pos != (0,1) and pos != (1,0):
                    hole_pos.append(pos)

        if level == 2:
            #4x5 grid, generates coords for gloves and holes
            gameboard = [['*' for x in range(5)] for y in range(4)]
            self.board = np.array(gameboard)
            while len(glove_pos) < 1:
                gpos = (random.randint(0,3),random.randint(0,4))
                if gpos != (0,0) and gpos != (1,0) and gpos != (0,1):
                    glove_pos.append(gpos)
            while len(hole_pos) < 8:
                pos = (random.randint(0,3),random.randint(0,4))
                #check that this coord isnt where the gloves are or ajacent to loggy start pos
                if pos not in hole_pos and pos not in glove_pos and pos != (0,0) and pos != (0,1) and pos != (1,0):
                    hole_pos.append(pos)

        if level == 3:
            #5x5 grid, coords for gloves and holes
            gameboard = [['*' for x in range(5)] for y in range(5)]
            self.board = np.array(gameboard)
            while len(glove_pos) < 1:
                gpos = (random.randint(0,4),random.randint(0,4))
                if gpos != (0,0) and gpos != (1,0) and gpos != (0,1):
                    glove_pos.append(gpos)
            while len(hole_pos) < 10:
                pos = (random.randint(0,4), random.randint(0,4))
                #check that this coord isnt where the gloves are or ajacent to loggy start pos
                if pos not in hole_pos and pos not in glove_pos and pos != (0,0) and pos != (0,1) and pos != (1,0):
                    hole_pos.append(pos)

        self.gloves = glove_pos
        self.holes = hole_pos


class Loggy:
    '''
    attributes of loggy..position and her stamina (num times can climb out of hole)
    '''
    def __init__(self,level):
        self.position = (0,0) #starts in top right corner
        self.stamina = 3*level  #she can climb out of a certain number of holes before she tires

def changepos(move, loggy):
    '''
    updates the location of loggy given user input and also returns the old position in a list
    '''
    if move == 'w':
        if loggy.position[0] == 0: #this one won't cause an index error, but still dont want it to move
            return []
        else:
            oldpos = loggy.position
            #move up
            newpos = (loggy.position[0]-1, loggy.position[1])
            return [oldpos,newpos]
    elif move == 'a':
        if loggy.position[1] == 0:
            return []
        oldpos = loggy.position
        #move left
        newpos = (loggy.position[0],loggy.position[1]-1)
        return [oldpos,newpos]

    elif move == 's':
        oldpos = loggy.position
        #move down
        newpos = (loggy.position[0]+1,loggy.position[1])
        return [oldpos,newpos]

    elif move == 'd':
        oldpos = loggy.position
        #move right
        newpos = (loggy.position[0], loggy.position[1]+1)
        return [oldpos,newpos]




def play():
    '''
    loops through the gameplay until the player has won, once they win, move to next level. If
    they lose, then the game will quit
    '''

    level = 1 #starts at level 1
    if sys.argv[1] == 'challenge':
        while level < 4:
            #loops through this for each level, new board for each
            has_won = False
            loggy = Loggy(level)
            board = Board(level) #creates board depending on level
            board.board[loggy.position] = 'L'
            print
            print 'Level', level
            print
            print board.board
            #loop until you win or lose a level
            while has_won == False and loggy.stamina > 0:
                #get raw input for movement
                possible = ['w','a','s','d', 'W', 'A', 'S','D','q','Q']
                print
                move = raw_input('Up (W), down (S), left (A), right (D), or quit (Q)? ')
                print
                #check to see if it is the correct input...
                while move not in possible:
                    print
                    print 'Please choose either W, A, S, D, or Q'
                    print
                    move = raw_input('Up (W), down (S), left (A), right (D), or quit (Q)? ')
                    print
                #use the input given to move Loggy
                move = move.lower()
                if move == 'q':
                    print
                    print 'Seeya next time!'
                    quit()
                #get a list of old and new pos, will be empty if cant go that way
                pos_update = changepos(move,loggy)
                if pos_update == []:
                    print board.board
                else:
                    oldpos = pos_update[0]
                    newpos = pos_update[1]

                    #update the board so it looks like loggy moved
                    #need try/except because errors will occur otherwise with going out of range of index when moving
                    try:
                        if oldpos in board.holes:
                            #shows where already-stepped-in holes are
                            board.board[newpos] = 'L' #put this before updating oldpos because it will cause the error and we dont want anything to change if the error occurs
                            board.board[oldpos] = 'O'
                        else:
                            board.board[newpos] = 'L'
                            board.board[oldpos] = ' '
                        loggy.position = newpos
                        print board.board
                        if loggy.position in board.gloves:
                            #check what level bc if level 3, then the game is all over, otherwise loops again
                            if level != 3:
                                has_won = True
                                level +=1
                                time.sleep(.5)
                                print
                                print '~*~*~**~*~*~*~*~*~*~*~*~*~*~**~*~*~*~*~*~*~*~'
                                print 'Congrats! You helped Loggy find her gloves...'
                                print 'Looks like she just lost them again in a bigger part of her yard, though!'
                                print '~*~*~**~*~*~*~*~*~*~*~*~*~*~**~*~*~*~*~*~*~*~'
                                print
                                break
                            else:
                                has_won = True
                                level += 1
                        elif loggy.position in board.holes:
                            loggy.stamina -= 1
                            time.sleep(.5)
                            print
                            print'----------------------------------------------------'
                            print 'Oh no! Loggy fell into a hole! Her stamina is now', loggy.stamina
                            print'----------------------------------------------------'
                            print
                    except IndexError:
                        print board.board
                        print
            if loggy.stamina == 0:
                print "Shoot! She's all tuckered out! Better try again next time!"
                quit()
        time.sleep(.5)
        print '~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~'
        print 'Holy crap! You found her gloves for the last time!! Congrats!'
        print
        print "You're the best! <{^-^}>"
        print '~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~'
        quit()
    elif sys.argv[1] == 'original':
        #'original' mode only has one level, and you win after just the first level
        level = 1
        has_won = False
        loggy = Loggy(level)
        board = Board(level) #creates board depending on level
        board.board[loggy.position] = 'L'
        print board.board
        #loop until you win or lose a level
        while has_won == False and loggy.stamina > 0:
            #get raw input for movement
            possible = ['w','a','s','d', 'W', 'A', 'S','D','q','Q']
            print
            move = raw_input('Up (W), down (S), left (A), right (D), or quit (Q)? ')
            print
            #check to see if it is the correct input...
            while move not in possible:
                print
                print 'Please choose either W, A, S, or D'
                print
                move = raw_input('Up (W), down (S), left (A), right (D), or quit (Q)? ')
                print
            #use the input given to move Loggy
            move = move.lower()
            if move == 'q':
                print
                print 'Seeya next time!'
                quit()
            #get a list of old and new pos, will be empty if cant go that way
            pos_update = changepos(move,loggy)
            if pos_update == []:
                print board.board
            else:
                oldpos = pos_update[0]
                newpos = pos_update[1]

                #update the board so it looks like loggy moved
                try:
                    if oldpos in board.holes:
                        #shows where already-stepped-in holes are
                        board.board[newpos] = 'L'
                        board.board[oldpos] = 'O'

                    else:
                        board.board[newpos] = 'L'
                        board.board[oldpos] = ' '
                    loggy.position = newpos
                    print board.board
                    print
                    if newpos in board.gloves:
                        has_won = True
                        level +=1
                        time.sleep(.5)
                        print
                        print '~*~*~**~*~*~*~*~*~*~*~*~*~*~**~*~*~*~*~*~*~*~'
                        print 'Congrats! You helped Loggy find her gloves...'
                        print "You're the best!!!"
                        print '~*~*~**~*~*~*~*~*~*~*~*~*~*~**~*~*~*~*~*~*~*~'
                        print
                        quit()
                    elif newpos in board.holes:
                        loggy.stamina -= 1
                        time.sleep(.5)
                        print
                        print'----------------------------------------------------'
                        print 'Oh no! Loggy fell into a hole! Her stamina is now', loggy.stamina
                        print'----------------------------------------------------'
                        print
                except IndexError:
                    print board.board
        if loggy.stamina == 0:
            print "Shoot! She's all tuckered out! Better try again next time!"
            quit()









if __name__ == '__main__':

    if len(sys.argv) == 1 or (sys.argv[1] != 'original' and sys.argv[1] != 'challenge'):
        print
        print 'Please indicate with an additional command line argument\nwhether you would like original mode (one level) or challenge mode (three levels)\nby entering either "original" or "challenge"'
        quit()
    else:

        print
        print '~*~*~*~*~*~*~*~*~'
        print 'WELCOME TO LOGGY!'
        print '~*~*~*~*~*~*~*~*~'
        print
        time.sleep(1)
        print 'Loggy is what her name suggests...A log!'
        print
        time.sleep(3)
        print 'Unfortunately for her, she has lost her gloves somewhere in the'
        print 'bushes of her backyard'
        print 'and needs to go find them...'
        print
        time.sleep(4)
        print 'And even MORE unfortunate is that the evil Drillers have come and drilled perfectly'
        print 'Loggy-shaped holes in her yard into which she may fall...'
        print
        time.sleep(5)
        print 'Luckily she has the strength to climb out of some of these,'
        print 'but will eventually grow too tired to continue'
        print
        time.sleep(4)
        print 'Help navigate Loggy (L) through her yard using WASD controls and avoid the holes to find her gloves!'
        print '~*~*~*~*~*~*~*~*~'
        print
        print
        time.sleep(2)

        play()
