# Mini-project #6 - Blackjack

import simplegui
import random

CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 600
# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")

# initialize some useful global variables
NUMBER_OF_CARDS_IN_HAND = 2
in_play = False
player_score = 0
dealer_score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank),
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)

# define hand class
class Hand:
    is_has_ace = False

    def __init__(self):
        self.cards_list = []

    def __str__(self):
        hand_str = 'Hand contains '
        for card in self.cards_list:
            hand_str += str(card)
            hand_str += ' '
        return hand_str[:-1]

    def add_card(self, card):
        if card.get_rank() == 'A':
            self.is_has_ace = True
        return self.cards_list.append(card)

    def get_value(self):
        self.total_hand_value = 0
        for card in self.cards_list:
            self.total_hand_value += VALUES[card.get_rank()]
        if self.is_has_ace and (self.total_hand_value + 10) <= 21:
            self.total_hand_value += 10
        return self.total_hand_value

    def draw(self, canvas, pos):
        for card in self.cards_list:
            card.draw(canvas, pos)
            pos[0] += CARD_SIZE[0]

# define deck class
class Deck:
    def __init__(self):
        self.cards_list = [Card(suite, rank) for suite in SUITS for rank in RANKS]

    def shuffle(self):
        return random.shuffle(self.cards_list)

    def deal_card(self):
        return self.cards_list.pop(0)

    def __str__(self):
        deck_str = 'Deck contains '
        for card in self.cards_list:
            deck_str += str(card)
            deck_str += ' '
        return deck_str[:-1]

#define event handlers for buttons
def deal():
    global control_text, in_play, current_deck, player_hand, dealer_hand, player_hand_value, dealer_hand_value, not_so_much_text_time, final_text_size
    if in_play:
        finish_game('Dealer')
        return
    current_deck = Deck()
    current_deck.shuffle()
    player_hand = Hand()
    dealer_hand = Hand()
    for num in range(NUMBER_OF_CARDS_IN_HAND):
        player_hand.add_card(current_deck.deal_card())
        dealer_hand.add_card(current_deck.deal_card())
    player_hand_value = player_hand.get_value() 
    dealer_hand_value = dealer_hand.get_value()
    control_text = 'Hit or Stand?'
    final_text_size = 1
    not_so_much_text_time = 1
    in_play = True

def hit():
    global in_play, player_hand_value

    if in_play:
        player_hand.add_card(current_deck.deal_card())
    player_hand_value = player_hand.get_value()
    if player_hand_value > 21 and in_play:
        finish_game('Dealer')

def stand():
    global in_play, player_hand_value, dealer_hand_value, final_text
    player_hand_value = player_hand.get_value()
    if player_hand_value > 21:
        final_text = 'Once again: you have busted:('
    elif in_play:
        dealer_hand_value = dealer_hand.get_value()
        while dealer_hand_value < 17:
            dealer_hand.add_card(current_deck.deal_card())
            dealer_hand_value = dealer_hand.get_value()
        if dealer_hand_value > 21 or dealer_hand_value < player_hand_value:
            finish_game('Player')
        else:
            finish_game('Dealer')

# draw handler
def draw(canvas):
    control_color = '#D1D1D1'
    logo_x = CANVAS_WIDTH/3
    logo_y = CANVAS_HEIGHT/2
    canvas.draw_text('Blackjack', [logo_x, logo_y], 50, control_color, 'monospace')

    control_panel_A = [0, CANVAS_HEIGHT-CANVAS_HEIGHT/3]
    control_panel_B = [CANVAS_WIDTH/2, CANVAS_HEIGHT-CANVAS_HEIGHT/3]
    control_panel_C = [CANVAS_WIDTH/2, CANVAS_HEIGHT]
    control_panel_D = [0, CANVAS_HEIGHT]
    canvas.draw_polygon([control_panel_A, control_panel_B, control_panel_C, control_panel_D], 2, control_color, control_color)

    control_panel_line_A = [control_panel_A[0], control_panel_A[1]+40]
    control_panel_line_B = [control_panel_B[0], control_panel_B[1]+40] 
    canvas.draw_polyline([control_panel_line_A, control_panel_line_B], 2, 'black')

    score_text = 'Dealer : Player  =  ' + str(dealer_score) + ' : ' + str(player_score)
    score_pos = [control_panel_A[0]+20, control_panel_A[1]+25]
    canvas.draw_text(score_text, score_pos, 20, 'black') 

    control_text_pos = [control_panel_D[0]+40, control_panel_C[1]-70]
    canvas.draw_text(control_text, control_text_pos, 45, 'black')

    dealer_hand_pos = [control_panel_B[0]+75, CANVAS_HEIGHT/8]
    dealer_back_hand_pos = [dealer_hand_pos[0]+CARD_BACK_CENTER[0], dealer_hand_pos[1]+CARD_BACK_CENTER[1]]
    dealer_hand.draw(canvas, dealer_hand_pos)
    if in_play:
        dealer_name_text = 'Dealer'
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, dealer_back_hand_pos, CARD_SIZE)
    else:
        dealer_name_text = 'Dealer' + ' = ' + str(dealer_hand_value)
    dealer_text_pos = [control_panel_B[0]+75, CANVAS_HEIGHT/8-20] 
    canvas.draw_text(dealer_name_text, dealer_text_pos, 25, 'white') 

    player_name_text = 'Player' + ' = ' + str(player_hand_value)
    player_name_pos = [control_panel_B[0]+75, control_panel_B[1]-20]
    canvas.draw_text(player_name_text, player_name_pos, 25, 'white')

    player_hand_pos = [control_panel_B[0]+75, control_panel_B[1]]
    player_hand.draw(canvas, player_hand_pos)

    if not in_play:
        result_text_pos = [logo_x-270, logo_y-150]
        canvas.draw_text(final_text, result_text_pos, final_text_size, 'yellow')
        if not_so_much_text_time > 50:
            canvas.draw_text(final_not_so_much_text, [result_text_pos[0], result_text_pos[1]+20], 15, 'black')

def finish_game(winner):
    global player_score, in_play, control_text, player_score, dealer_score

    if winner == 'Player':
        set_final_text('Player')
        player_score += 1
    elif winner == 'Dealer':
        set_final_text('Dealer')
        dealer_score += 1
    else:
        print 'Unknown player: ', winner
    control_text = 'Deal new game?'
    in_play = False

def set_final_text(winner):
    global final_text, final_not_so_much_text

    player_win_text = ['10 POINTS TO GRYFFINDOR!', 'GRYFFINDOR WIN!', 'AVE, PLAYER!', 'YOU MY GOD, PLAYER!', 'You win!']
    player_not_so_much_win_text = ['just kidding. 1 point to Slytherin. Snape', 'just kidding. 1 point to Slytherin. Snape', 'just kidding. dealer has money', 'just kidding. hiiiighway to hell!', 'just kidding. hm-hm, no, not kidding.']
    dealer_win_text = ['WASTED!', 'YOU HAVE BUSTED!', 'YOU LOST!']
    dealer_not_so_much_win_text = ['don\'t be upset. you can lose next time again.', 'don\'t be upset. winning isn\'t everything. looser.', 'don\'t be upset. you\'re beautiful. momma']

    if winner == 'Player':
        final_text = random.choice(player_win_text)
        final_not_so_much_text = player_not_so_much_win_text[player_win_text.index(final_text)]
    elif winner == 'Dealer':
        final_text = random.choice(dealer_win_text)
        final_not_so_much_text = dealer_not_so_much_win_text[dealer_win_text.index(final_text)]
    else:
        print 'Unknown player: ', winner
    final_not_so_much_text = '(' + final_not_so_much_text + ')'

def tick():
    global final_text_size, not_so_much_text_time

    if not in_play:
        if final_text_size < 38:
            final_text_size += 0.4
        else:
            not_so_much_text_time += 1

# initialization frame
frame = simplegui.create_frame("Blackjack", CANVAS_WIDTH, CANVAS_HEIGHT)
frame.set_canvas_background("Green")
final_text_size_timer = simplegui.create_timer(13, tick)

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
final_text_size_timer.start()
frame.start()


# remember to review the gradic rubric
