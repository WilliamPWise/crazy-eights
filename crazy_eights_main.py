#!/usr/bin/env python3
import random, os

#important functions

def input_number(text="", error_text=""):
	
	'''Returns a user's input as an integer instead of a string, asks for input again if the input isn't an integer.'''
	
	user_input = input(text)
	
	while True:		
		
		try:
			num_input = int(user_input)
			break
		
		except ValueError:
			user_input = input(error_text)
			
	return num_input 


def new_deck():
	
	"""Builds a full deck of 52 Playing Cards"""
	
	deck = []
	card_nums = [ '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace' ]
	card_suits = [ 'Spades', 'Hearts', 'Clubs', 'Diamonds' ]
	for card in card_nums:
		for suit in card_suits:
			deck.append(card + " of " + suit)
	return deck


def draw_cards(num_of_cards, card_deck):	
	
	"""Returns a list of drawn cards, removes them from the deck"""
	
	cards_drawn = []
	for card in range(num_of_cards):
		cards_drawn.append(card_deck[0])
		del card_deck[0]
	return cards_drawn


def is_card_playable(card):	
	
	'''Checks to see if the card value can be played into the discard pile, returns True if so, and False if not.'''
	
	card_value = False
	card_attributes = card.split(" of ")
	card_name = card_attributes[0]
	card_suit = card_attributes[1]
	
	if card_name in discard_pile[-1] or card_suit in discard_pile[-1] or card_name == "8":
		card_value = True
	
	return card_value


def playable_cards(hand):
	
	'''Returns a list of all the cards a player can play during their turn.'''
	
	play_list = []
	for card in hand:
		if is_card_playable(card) == True:
			play_list.append(card)
	return play_list


def selected_card(player):
	
	'''Returns the card that the player will play during their turn. For the user, it gives input to choose the card that this function returns, and a dialogue loop for an invalid choice.'''
	
	error_text = "That's not a valid choice. Type the number next to the card to select it, then press enter. "
	while player == "You":
		
		selection = input_number("", error_text)		
		if 1 <= selection <= len(player_hands[player]):
			card_select = player_hands[player][selection - 1]
			if card_select in playable_cards(player_hands[player]):
				break				
			else:
				print("\nThat's not a playable card! Try again. ")
		
		else:
			print(error_text)
	
	if player != "You":
		card_select = playable_cards(player_hands[player])[0]
	
	return card_select


def mulligans(list_option=""):
	
	'''Returns a number of cards to draw if the player has no playable cards. Optionally, it can return the list of mulligan cards to be drawn instead.'''
	
	new_cards = []
	draw_count = 0
	
	while playable_cards(new_cards) == []:
		if draw_count >= len(card_deck):
			break
		new_cards.append(card_deck[draw_count])
		draw_count += 1
	
	if list_option == "list":
		return new_cards
	else:
		return draw_count

def proxy_suit(player):
	
	'''Returns a string that acts as a suit changer when an eight card gets played. It gets used like a card proxy on the discard pile.'''
	
	suits = ["Spades", "Hearts", "Clubs", "Diamonds"]
	if player == "You":
		message = "What suit would you like to change it to?\n\n|1|: Spades |2|: Hearts |3|: Clubs |4|: Diamonds"
		error_message = "Type the number next to the suit you want, and press enter."
		suit_choice = input_number(message, error_message)
		
		while suit_choice != "" and 0 > int(suit_choice) > 5:
			suit_choice = input_number(error_message, error_message)
		
		return suits[suit_choice - 1]
	
	else:
		return suits[card_mixer.randrange(4)]


def mulligan_text(player, mulligans, mulligan_list):
	
	'''Returns or displays text for when a player has to draw from the deck.'''
	
	if player == "You":
		confirm = input("You have no playable cards this turn! Press enter to draw from the deck. ")
		text = "This is what you drew:\n\n"
		for card in mulligan_list:
			text += card + "\n"

		if playable_cards(mulligan_list) > []:
			text += "\nPress enter to play the last card you drew. "
			confirm2 = input(text)
			return ""
		
		else:
			return text
		
	elif mulligans == 1:
		return player + " had to draw a card!/n"
		
	elif mulligans >= 2:
		return player + " had to draw " + str(mulligans) + " cards!/n"
	
	else:
		return ""	


def cardplay_text(player):
	
	'''Returns text to be printed when a card is played.'''
	
	text = player + " played a"
	
	if "8" in discard_pile[-1] or "Ace" in discard_pile[-1]:
		text += "n" 
	
	text += " **" + discard_pile[-1] + "!**\n"
	
	if player != "You":
		hand_size = len(player_hands[player])
		text += "Cards Remaining: " + str(hand_size) + "\n"

	return text
	
	
def passing_text(player):
	
	'''Returns text for when a player has to pass their turn'''
	
	if player == "You":
		confirm = input("/n Sorry, the deck is empty, and you have no playable cards. Press enter to pass this turn.")
		return ""
	else:
		return player + " couldn't play any cards and had to pass this turn!"


def ui_text(player):
	
	'''Returns the generic user interface text for the user's turn. It shows all the cards in the user's hand in the process''' 
		
	text = "It's your turn!"
	
	if playable_cards(player_hands[player]) > []:
		text += " Select a card to play:"
	else:
		text += " This is your hand:"
		
	text += "\n\n"
	card_number = 1
	for card in player_hands[player]:
		text += "|" + str(card_number) + "|: " + card + "\n"
		card_number += 1
		
	return text


def clean_the_screen(player="You"):
	
	'''A simple function to clean the screen after each round of turns.'''
	
	if player == "You":
		os.system('cls' if os.name == 'nt' else 'clear')


def player_turn(player, card_deck, discard_pile):
	
	if player == "You":
		print(ui_text(player) )
	
	if playable_cards(player_hands[player]) > []:
		card_select = selected_card(player)
				
	if playable_cards(player_hands[player]) == [] and card_deck > []:
		
		print( mulligan_text(player, mulligans(), mulligans("list") ) )
		player_hands[player] += draw_cards(mulligans(), card_deck)
		if playable_cards(player_hands[player]) > []:
			card_select = playable_cards(player_hands[player])[0]
		
	if playable_cards(player_hands[player]) == [] and card_deck == []:
		print(passing_text(player))
		return None
	
	discard_pile.append(card_select)
	player_hands[player].remove(card_select)
	
	if "8" not in discard_pile[-1]:	
		clean_the_screen(player)
		
	print(cardplay_text(player))
	
	if "8" in discard_pile[-1]:
		discard_pile.append(proxy_suit(player))
		clean_the_screen(player)
		print("The suit is now " + discard_pile[-1] + "!\n")


# ***-----The Main Gameplay Code!-----***

# Set up the active players, their hands, and their scorecards.

player_names = ["You", "Player 2", "Player 3", "Player 4", "Player 5"]
active_players = []
player_hands = {}
scorecards = {}

greet_text = "***Welcome to the Crazy Eights Program!***\n\nHow many players would you like? "
error_text = "Choose between 2, 3, 4, or 5 Players! "
num_of_players = input_number(greet_text, error_text)

while True:
	
	if 5 >= num_of_players >= 2:
		for index in range(num_of_players):
			
			active_players.append(player_names[index])
			player_hands[player_names[index]] = []
			scorecards[player_names[index]] = 0
			
		break
	
	else:
		num_of_players = input_number(error_text, error_text)
		
# ****The Primary Game Loop****

while True:

	# Set up the deck and shuffle it. 
	
	card_deck = new_deck()
	card_mixer = random.Random()
	card_mixer.shuffle(card_deck)
	
	# Deal the cards to each player.
	
	for hand in player_hands.keys():
		if num_of_players == 2:
			player_hands[hand] += draw_cards(7, card_deck)
		else:
			player_hands[hand] += draw_cards(5, card_deck)
	
	# Set up the discard pile and its starting card. 
		
	discard_pile = []
	discard_pile += draw_cards(1, card_deck)
	
	print("\nA round has now started! The starting card is a **" + discard_pile[0] + "**!\n")
	
	# If the starting card was an 8, place it back in the deck and draw a new card.
	
	while True:
		if "8" in discard_pile[0]:
			card_deck.insert(-1, discard_pile.pop())
			discard_pile += draw_cards(1, card_deck)
			print("Oops! Let's try a diferent card. This time, it's a " + discard_pile[0] + "!\n")
		else: 
			card_mixer.shuffle(card_deck)
			break
	
	# The user always goes first for the first round.  
	
	if active_players[0] == "You":
		print("You get to go first!\n")
	else:
		print(active_players[0], "gets to begin this game!\n")
	
	# Set up the sequence of turns in a loop.
	
	player_index = 0
	while True:	
		active_player = active_players[player_index]
		player_turn(active_player, card_deck, discard_pile) # This function contains all the actions of a player taking a turn.
		player_index += 1
		
		if player_index == len(active_players):
			player_index = 0
			
		# If a player played all their cards, send a winning message!
		 	
		if player_hands[active_player] == []:
			winner = active_player
			if winner == "You":
				print("**Congratulations! You cleared your hand and have won this round!**\n")
			else:
				print(winner, "has no more cards, and has won this round!\n")
			break
	
	# Display the point values of each card:

	confirm = input("Press enter to tally up the score. ")
	clean_the_screen()
	
	scorecard_points = { "Ace": 1, "King": 10, "Queen": 10, "Jack": 10, "10": 10, "9": 9, "8": 50, "7": 7, "6": 6, "5": 5, "4": 4, "3": 3, "2": 2 }	
	
	print("Here are the point values of each card:\n")
	print_interval = 0
	for point_value in scorecard_points.keys():
		print("| ", point_value + " -->", scorecard_points[point_value], "points  ", end='')
		print_interval += 1
		if print_interval == 4:
			print("|\n", end='')
			print_interval = 0
		
	# Add up the points given to the winner, according to the cards in each player's hands.
	
	print("\n\nHere are the cards left in each player's hand:\n")
	
	round_total = 0
	
	for player in active_players:
		
		if player != winner:
			print(player + ":\n")
			for card in player_hands[player]:
				print(card)
			print("")
			
		for card in player_hands[player]:
			
			for point_value in scorecard_points.keys():
				if point_value in card:
					scorecards[winner] += scorecard_points[point_value]
					round_total += scorecard_points[point_value]	 
					
		# Clean up each player's hands for the next round.
		
		player_hands[player] = []
			
	print(winner, "gained", round_total, "points this round! Here's the current score:\n")
	for player in active_players:
		print(player + ":", scorecards[player], "\n")
	
	# If a player hits 200 points, the player wins the game, and the program closes.
	
	end_game = False
	
	for player in active_players:	
		if scorecards[player] >= 200:
			print(player, "surpassed 200 points!")
			if player == "You":
				print("*****Very well done - You won the game!*****")
			else:
				print(player, "won the game. Better luck next time!")
			exit_confirm = input("Press enter to close the game. Thank you for playing!")
			end_game = True
			
	if end_game == True:
		break		
	
	# Otherwise, set up the next round, and rotate the order of who goes first.
	
	confirm = input("Press enter to begin the next round!")
	active_players.append(active_players.pop(0))
	clean_the_screen()
