#Model objects 
from deck_of_cards import Card, Hand, Deck

#General imports
import sys
from numpy.random import shuffle

#For doing stats and making graphs
import matplotlib.pyplot as plt
import numpy as np
import scipy
from scipy.stats import describe

#Constants!
NUM_TRIALS = 10
NUM_SIMULATIONS = 10000
MAX_MOVES = 10000
CARDS_PER_HAND = 26
HI_COMEBACK = 10
LO_COMEBACK = 5


def write_moves(verbal_moves, trial_number):
#Write out moves to file
    with open(str(run_number)+"_moves.txt", 'w') as f:
        for move in verbal_moves:
            print >> f, move



def write_stats(num_lo_comebacks, num_hi_comebacks, stats, median, trial_number):
#Write out the stats and number of comebacks to file
    
    with open(str(trial_number)+"_stats.txt", 'w') as f:
        f.write("Number of "+str(LO_COMEBACK)+" comebacks: "+str(num_lo_comebacks)+"\n")
        f.write("Number of "+str(HI_COMEBACK)+" comebacks: "+str(num_hi_comebacks)+"\n")    
        print >> f, stats
        f.write("Median: "+str(median))
        f.write("\n")



def make_histogram(move_counts, trial_number):
#Create and save a relative frequency histogram of the number of moves
    move_counts = np.array(move_counts)

    plt.clf()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.hist(move_counts, weights = np.zeros_like(move_counts)+1./ move_counts.size, bins = 50)
    plt.title("Number of moves in 10,000 game War simulation")
    plt.xlabel("Number of moves")
    plt.ylabel("Frequency")
    plt.savefig(str(trial_number)+"_histo.png")



def check_for_comebacks(player, num_lo_comebacks, num_hi_comebacks):
    if player.lo_comeback:
        num_lo_comebacks += 1

    elif player.hi_comeback:
        num_hi_comebacks += 1

    return(num_lo_comebacks, num_hi_comebacks)



def check_cards(player):
    #Check if a player's hand dips below five or ten cards, signalling they made
    #a 'comeback'

    num_cards = len(player.cards)

    if num_cards <= HI_COMEBACK:
        if num_cards > LO_COMEBACK:
            player.hi_comeback = True
        else:
            player.lo_comeback = True



def declare_war(p1, p2, c1, c2, verbal_moves):
    loot = [c1, c2]
    v1, v2 = c1.value, c2.value

    while (v1 == v2):
    #Playing the version where if you have less than three cards, you place 
    #as many as you can as 'loot' and then flip your last card
 
        if (len(p1.cards) > 3 and len(p2.cards) > 3):
            for i in range(3):
                loot.append(p1.flip())
                loot.append(p2.flip())

        elif len(p1.cards) < 3:
            while len(p1.cards) > 1:
                loot.append(p1.flip())
        
        else:
            while len(p2.cards) > 1:
                loot.append(p2.flip())
        
        #A player may go down to their last card in multiple rounds of war
        #Flip it, reveal another tie, and get here with an empty hand. 
        #In this case, the player with remaining cards wins. 
        #The code here accounts for that scenario.         

        try:
            c1 = p1.flip()
        except IndexError:
            verbal_moves.append("Player 1 has run out of cards in war!")
            p2.gain(loot)
            return

        try:
            c2 = p2.flip()
        except IndexError:        
            verbal_moves.append("Player 2 has run out of cards in war!")
            p1.gain(loot)       
            return

        verbal_moves.append("P1 wars "+str(c1)+" against P2 "+str(c2))
        v1, v2 = c1.value, c2.value
        loot += [c1, c2]

    shuffle(loot)
   
    if v1 > v2:
        p1.gain(loot)        

    else: 
        p2.gain(loot)    



def play_war(p1, p2, max_moves, long_game_flag, trial_number):
    moves = 0
    verbal_moves = []

    while (p1.cards and p2.cards) and (moves < max_moves):
        moves += 1
        verbal_moves.append("P1 has "+str(len(p1.cards))+" cards, P2 has "+str(len(p2.cards)))
        c1 = p1.flip()
        c2 = p2.flip()
        check_cards(p1)
        check_cards(p2)
        verbal_moves.append("P1 plays "+str(c1)+" against P2 "+str(c2))

        v1, v2 = c1.value, c2.value
        if v1 > v2:
            p1.gain([c1, c2])            

        elif v2 > v1:
            p2.gain([c2, c1])

        else:
            verbal_moves.append("It\'s war!")
            declare_war(p1, p2, c1, c2, verbal_moves)
            moves += 1

    #Original code in which winner and number of moves were printed to shell
    if 0:
        print("Total num of moves is "+str(moves))
        if p1.cards:
            return("1")

        return("2")

    #We want to write out one infinite game per trial
    #After one game is written out, the flag is flipped to avoid getting here
    if (moves == MAX_MOVES and not long_game_flag):
        write_moves(verbal_moves, trial_number)
        long_game_flag = 1

    return(moves, long_game_flag)



def main(argv):
    if len(argv) > 1:
        max_moves = int(argv[1])
        num_simulations = int(argv[2])

    else:
        max_moves = MAX_MOVES
        num_simulations = NUM_SIMULATIONS    
    
    for i in range(NUM_TRIALS):
        all_move_counts = [] 
        num_lo_comebacks = 0
        num_hi_comebacks = 0   
        long_game_flag = 0

        for j in range(num_simulations):
            new_deck = Deck()
            player1 = Hand(new_deck, CARDS_PER_HAND)
            player2 = Hand(new_deck, CARDS_PER_HAND)
            moves, long_game_flag = play_war(player1, player2, max_moves, long_game_flag, i)
            all_move_counts.append(moves)

            if player1.cards:
                num_lo_comebacks, num_hi_comebacks = check_for_comebacks(player1, num_lo_comebacks, num_hi_comebacks)

            else:
                num_lo_comebacks, num_hi_comebacks = check_for_comebacks(player2, num_lo_comebacks, num_hi_comebacks)
        
        #Describe is imported scipy and reports the number of observations, min and max, mean, variance, skewness, and kurtosis    
        descriptive_stats = describe(all_move_counts)
        median = np.median(all_move_counts)
        write_stats(num_lo_comebacks, num_hi_comebacks, descriptive_stats, median, i)
        make_histogram(all_move_counts, i)      

# From initial version: for printing out the winner
#    winner = play_war(player1, player2)
#    print("Player "+winner+" won!")


if __name__ == "__main__":
    main(sys.argv)
