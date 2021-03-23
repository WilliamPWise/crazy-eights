#!/usr/bin/env python3
import random, os

#important functions
def clean_the_screen():
	
	'''A simple function to clean the screen after each round of turns.'''
	
	os.system('cls' if os.name == 'nt' else 'clear')


def new_deck():
	
	"""Builds a full deck of 52 Playing Cards"""
	
	deck = []
	card_nums = [ '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace' ]
	card_suits = [ 'Spades', 'Hearts', 'Clubs', 'Diamonds' ]
	for card in card_nums:
		for suit in card_suits:
			deck.append(card + " of " + suit)
	return deck


def draw_cards(num_of_cards):	
	"""Returns a list of drawn cards, removes them from the deck"""
	
	cards_drawn = []
	for card in range(num_of_cards):
		cards_drawn.append(card_deck.pop())
	return cards_drawn


def reshuffle_deck():
	global card_deck
	'''Shuffles the Discard pile back into the deck, while removing any suit proxies and keeping the last played card'''
	
	proxy_cards = ["Spades", "Hearts", "Clubs", "Diamonds"]
	last_card = discard_pile.pop(-1)
	
	if last_card in proxy_cards: # If the last card is an 8, this makes sure the 8 and the proxy doesn't get shuffled back in. 
		last_proxy = last_card
		last_card = discard_pile.pop(-1)
	
	for card in discard_pile:
		card_deck.append(discard_pile.pop())
	
	for proxy in proxy_cards:
		for card in card_deck:
			if card == proxy:
				card_deck.remove(proxy)
	
	card_mixer.shuffle(card_deck)
	discard_pile.append(last_card)
	
	if "8" in last_card:
		discard_pile.append(last_proxy)
		
	print("*No more cards were left in the deck! Discarded cards were shuffled back in.* \n")


def is_card_playable(card):	
	'''Checks to see if the card value can be played into the discard pile, returns True if so, and False if not.'''
	
	card_value = False
	card_attributes = card.split(" of ")
	card_type = card_attributes[0]
	card_suit = card_attributes[1]
	
	if card_type in discard_pile[-1] or card_suit in discard_pile[-1] or card_type == "8":
		card_value = True
	
	return card_value


def cpu_turn(player):
	global discard_pile
	'''Recreates the events of a turn taken by computer players'''
	
	# Check to see if there are any playable cards, and list them out temporarily.
	
	playable_cards = []
	can_play = False
	for card in player_hands[player]:
		if is_card_playable(card) == True:
			playable_cards.append(card)
			can_play = True
	
	# If there are no available cards, draw cards until a playable one is found.
	
	draw_count = 0
	
	while can_play == False:
		
		if card_deck == []:
			reshuffle_deck()
			
		player_hands[player] += draw_cards(1)
		draw_count += 1
		new_card = player_hands[player][-1]
		if is_card_playable(new_card) == True:
			playable_cards.append(new_card)
			can_play = True
				
	
	discard_pile.append(playable_cards[0])
	player_hands[player].remove(playable_cards[0])
	
	# Dialogue of the cpu turn 
	
	if draw_count == 1:
		print(player, "had to draw a card!")
	if draw_count >= 2:
		print(player, "had to draw", draw_count, "cards!")
		
	print(player, "played a", "**" + discard_pile[-1] + "**!")
	print("Cards remaining:", len(player_hands[player]), "\n")
	
	if "8" in discard_pile[-1]:
		suits = ["Spades", "Hearts", "Clubs", "Diamonds"]
		proxy_suit = suits[card_mixer.randrange(4)]  # Cpu players choose a random suit!		
		discard_pile.append(proxy_suit)
		print("The suit is now", proxy_suit + "!\n")
		

def user_turn(player):
	global discard_pile
	'''Creates dialogue and input for the user to play a card during their turn'''
	
	# The generic interface
	
	print("Choose a card to play:\n")
	card_number = 1
	can_play_hand = False
	for card in player_hands[player]:
		print("|" + str(card_number) + "|:", card)
		card_number += 1	
		if is_card_playable(card) == True:
			can_play_hand = True

	# Conditions if the player's hand has at least one playable card. 
	
	while can_play_hand == True:
		
		selection = int(input("\n"))
		
		if 1 <= selection <= card_number:			
			card_select = player_hands[player][selection - 1]						
			if is_card_playable(card_select) == True:					
				discard_pile.append(card_select)
				player_hands[player].remove(card_select)		
				break				
			else:
				print("\nThat's not a playable card! Try again. ")
		
		else:
			print("\nThat's not a valid choice. Type the number next to the card to select it, then press enter. ")
	
	# If there were no playable cards in the first place, cards are auto-drawn and played.
	
	if can_play_hand == False:
		
		draw_confirmation = input("\nYou have no playable cards! Press enter to draw from the deck. ")
		print("This is what you drew:\n")
		draw_count = 0
		
		while True:
			
			if card_deck == []:
				reshuffle_deck()
			
			player_hands[player] += draw_cards(1)
			draw_count += 1
			new_card = player_hands[player][-1]
			print(new_card)
			
			if is_card_playable(new_card) == True:
				confirmation = input("\nPress enter to play the last card you drew. ")
				discard_pile.append(new_card)
				player_hands[player].remove(new_card)
				break
		
	if "8" in discard_pile[-1]:
		suits = ["Spades", "Hearts", "Clubs", "Diamonds"]
		print("\n" + player, "played an", "**" + discard_pile[-1] + "**!\n")
		print("What suit would you like to change it to?\n")
		print("|1|: Spades |2|: Hearts |3|: Clubs |4|: Diamonds")
		while True:
			suit_choice = int(input())
			if 1 <= suit_choice	<= 4:
				proxy_suit = suits[suit_choice - 1]
				break
			else:
				print("Type the number next to the suit you want, and press enter.")
		
		discard_pile.append(proxy_suit)
		clean_the_screen()
		print("\nThe suit is now", proxy_suit + "!\n")
	
	else:
		clean_the_screen()
		print("\n" + player, "played a", "**" + discard_pile[-1] + "**!\n") 
		


# ***-----The Main Gameplay Code!-----***



# Set up the active players, their hands, and their scorecards.

player_names = ["You", "Player 2", "Player 3", "Player 4"]
active_players = []
player_hands = {}
scorecards = {}


print("***Welcome to the Crazy Eights Program!***\n")
num_of_players = int(input("How many players would you like? "))

while True:
	
	if 4 >= num_of_players >= 2:
		for index in range(num_of_players):
			active_players.append(player_names[index])
			player_hands[player_names[index]] = []
			scorecards[player_names[index]] = 0
		break
	
	else:
		num_of_players = int(input("Choose between 2, 3, or 4 Players! "))
		
# ****The Primary Game Loop****

while True:

	# Set up the deck and shuffle it. 
	
	card_deck = new_deck()
	card_mixer = random.Random()
	card_mixer.shuffle(card_deck)
	
	# Deal the cards to each player.
	
	for hand in player_hands.keys():
		player_hands[hand] += draw_cards(5)
	
	# Set up the discard pile and its starting card. 
		
	discard_pile = []
	discard_pile += draw_cards(1)
	
	print("\nA round has now started! The starting card is a **" + discard_pile[0] + "**!\n")
	
	# If the starting card was an 8, place it back in the deck and draw a new card.
	
	while True:
		if "8" in discard_pile[0]:
			card_deck.insert(0, discard_pile.pop())
			discard_pile += draw_cards(1)
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
		if active_player == "You":
			user_turn(active_player)
		else:
			cpu_turn(active_player)
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
