import sys

letters = [" ","A","B","C","D","E","F","G","H","I","J"] # this list for creating the table

out_file = open("Battleship.out","w")

def print_to_the_file_and_terminal(text, sep_value = " ", end_value="\n"):  # this function is for avoid unnecesesary two print function
	print(text,sep=sep_value,end=end_value)
	print(text,sep=sep_value,end=end_value,file=out_file)

def checking_for_integer(value):  # this function find if the value is integer or not
	try:
		value=int(value)
	except ValueError:
		return False
	else:
		return True

def file_read():  # rading the all files and dealing with the errors 
	ErrorList = []  # this list will be used for determine the wrong files and list them
	index = None
	global optional_player1,optional_player2,player1_ships,player2_ships,player1_in,player2_in
	with open("Player1.txt","r") as file:
		optional_player1 = file.read()
	with open("Player2.txt","r") as file:
		optional_player2 = file.read()
	try:
		try: # openning every file and catching the IOErrors, IndexError will be handled at the end of the function
			index = 1
			with open(sys.argv[1],"r") as file:  # sys.argv[1] -> Player1.txt which shows the ships (e.g. ;;;;;C;)
				player1_ships = file.read()
		except IOError:
			ErrorList.append(index)
		try:
			index = 2
			with open(sys.argv[2],"r") as file:  # sys.argv[2] -> Player2.txt which shows the ships (e.g. ;;;;;C;)
				player2_ships = file.read()
		except IOError:
			ErrorList.append(index)
		try:
			index  = 3
			with open(sys.argv[3],"r") as file:  # sys.argv[3] -> Player1.in which shows the shoots (e.g. 5,E;10,G)
				player1_in = file.read()
		except IOError:
			ErrorList.append(index)
		try:
			index = 4
			with open(sys.argv[4],"r") as file:  # sys.argv[4] -> Player2.in which shows the shoots (e.g. 5,E;10,G)
				player2_in = file.read()
		except IOError:
			ErrorList.append(index)
		if ErrorList != []:
			string_error_list = [sys.argv[t] for t in ErrorList]
			string_errors = ""  #  wrong files names added into a string to list them
			for error in string_error_list:
				string_errors = string_errors + error + " "
			raise IOError
	except IndexError:  # handling the IndexError
		print_to_the_file_and_terminal("IndexError: You have entered less file name than required.")
	except IOError:  # listing the IOErrors
		print_to_the_file_and_terminal("IOError: input file(s) {}is/are not reachable.".format(string_errors))
	except:  # All other errors
		print_to_the_file_and_terminal("kaBOOM: run for your life!")
	else:
		return True

# creates a dictionary for storing the data
def create_board():                               # { 0: { " ": "0", "A": "A", "B": "B" .....}
	board_dict = {}                               #   1: { " ": "1", "A": "O", "B": "O" .....}
	for i in range(11):                           #   2: { " ": "2", "A": "O", "B": "O" .....}
		rows_dict = {}                            #   .
		if i == 0:                                #   .
			for letter in letters:                #   .
				if letter==" ":                   #   10:{ " ": "10", "A":"O", "B":"O" ......} }
					rows_dict[letter] = 0
				else:
					rows_dict[letter] = letter
		else:
			for letter in letters:
				if letter==" ":
					rows_dict[letter] = i
				else:
					rows_dict[letter] = "-"
		board_dict[i] = rows_dict
	return board_dict


def adding_input_to_the_board(board_name,file):  # adding ship information to the board
	file_lines = file.split("\n") # splitting ship input line by line
	try:
		for line in file_lines:
			if line.count(";") != 9: #  this one is for if there is more space than 10 or more ships
				raise IndexError
			for char in line:
				if char not in [";","C","B","P","S","D"]:  # if there is other character
					raise ValueError
	except IndexError:
		print_to_the_file_and_terminal("IndexError: There is a mistake in ships location input file. Please review it again.")
	except ValueError:
		print_to_the_file_and_terminal("ValueError: There is wrong character in ships location input file. Please review it again.")
	except:
		print_to_the_file_and_terminal("kaBOOM: run for your life!")
	else:
		for t,line in enumerate(file_lines):
			for i,char in enumerate(line):
				if char != ";":
					index = line.count(";",0,i)+1
					board_name[t+1][letters[index]] = char  # adding board the axact locatin of the ship


def listing_the_shots(file):  # listing shots beacuse handling the errors before the rounds begin and clearing the shots
	all = file.split(";")[:-1]  # splitting shots from ";",  last ";" is unnecesesary
	shoot_list = []  # this list will have all the shots that player will took
	
	for i,member in enumerate(all):  
		try:    
			piece = member.split(",") # splitting from the "," and determining if the coordinates given right
			if len(member) == 0: # ;;  if there is nothing between ";"
				raise IndexError("IndexError: You have write \";\" two times or haven't add any coordinates. Please fix that. '{}' at the {}. member".format(member,i+1))

			elif len(piece) == 1: #  if there is only one member which is not a comma
				if checking_for_integer(member): # ;1; if that member is integer
					raise ValueError("IndexError: You haven't entered the y value and forget a comma. Please edit the file and add the x value. '{}' at the {}. member".format(member,i+1))
				else: # ;A;  if that member is string
					raise ValueError("IndexError: You haven't entered the x value and forget a comma. Please edit the file and add the y value. '{}' at the {}. member".format(member,i+1))

			elif len(piece) == 2:  # if there is one comma
				if piece[0] == '': # if the first member is empty
					if piece[1] == '': # ;,;  if also the second member is empty
						raise IndexError("IndexError: You haven't entered the x and y values. Please write them in the input file. '{}' at the {}. member".format(member,i+1))
					elif not checking_for_integer(piece[1]): # ;,A;  if second member is string
						raise IndexError("IndexError: You haven't entered the x value. Please write the x value in the input file. '{}' at the {}. member".format(member,i+1))
					elif checking_for_integer(piece[1]): # ;,1;  if the second member is integer
						raise IndexError("IndexError: You haven't entered the x value and you have entered the y value wrong, y value should be a letter Please edit your input file. '{}' at the {}. member".format(member,i+1))
				elif checking_for_integer(piece[0]):  # if the first member is integer
					if piece[1] == '': # ;1,; if the second member is empty
						raise IndexError("IndexError: You haven't entered the y value. Please write the y value in the input file. '{}' at the {}. member".format(member,i+1))
					elif checking_for_integer(piece[1]): # 1;1  if the second member is integer
						raise ValueError("ValueError: You have entered the wrong y value, y value should be a letter, Please edit your input file. '{}' at the {}. member".format(member,i+1))
					elif not checking_for_integer(piece[1]): # 1;A correct  if the second member is letter ehich is correct form
						if int(piece[0]) < 11:  # 10;K correct  if first member smaller than 11 which is correct
							if piece[1] in letters: # 10;J correct  if the second member is in the letter list
								shoot_list.append(piece)
							else: # 10;K letter wrong  if the letter not in letter list
								raise AssertionError("AssertionError: Invalid Operation. y value too high. '{}' at the {}. member".format(member,i+1))
						else: # 11;J number wrong  if the first member bigger than 10
							raise AssertionError("AssertionError: Invalid Operation. x value too high. '{}' at the {}. member".format(member,i+1))
				elif not checking_for_integer(piece[0]):  # if the first member is letter
					if piece[1] == '': # A;  if the second member is empty
						raise ValueError("ValueError: You have entered the wrong x value and you haven't entered the y value, x value should be a integer. Please edit your input file. '{}' at the {}. member".format(member,i+1))
					elif checking_for_integer(piece[1]): # A;1  if the second member is integer
						raise ValueError("ValueError: You have entered the wrong x and y value, x value should be a integer and y value should be a letter. Please edit your input file '{}' at the {}. member".format(member,i+1))
					elif not checking_for_integer(piece[1]): # A;A  if the second member is letter
						raise ValueError("ValueError: You have entered the wrong x value, x value should be a integer. Please edit your input file '{}' at the {}. member".format(member,i+1))

			elif len(piece)>2: # 5,E10,G;  if you forget a ";"
				raise ValueError("ValueError: Maybe you forget a ';' between coordinates. Please edit your input file. '{}' at the {}. member".format(member,i+1))
		except IndexError as e:  #  printing messages
			print_to_the_file_and_terminal(e)
		except ValueError as e:
			print_to_the_file_and_terminal(e)
		except AssertionError as e:
			print_to_the_file_and_terminal(e)
		except:  # in case of any other exception
			print_to_the_file_and_terminal("kaBOOM: run for your life!")
	return shoot_list


def optional_player(file,ships_dict):  # reading the optional files
	ship = file.split(":")[0]
	start_coordinate = file.split(":")[1].split(";",1)[0]
	x_cord = start_coordinate.split(",")[0]
	y_cord = start_coordinate.split(",")[1]
	coordinates = []
	
	if ship[0] == "B":  # only examine battleship and patrol boat
		ship_name = "Battleship {}".format(ship[1])
	elif ship[0] == "P":
		ship_name = "Patrol Boat {}".format(ship[1])

	
	if file.split(":")[1].split(";",1)[1] == "right;":  # if right
		for i,letter in enumerate(letters):
			if start_coordinate.split(",")[1] == letter:
				index = i

		if "Battleship" in ship_name:
			for t in range(4):
				coordinates.append("{},{}".format(x_cord,letters[index+t]))
		
		if "Patrol Boat" in ship_name:
			for t in range(2):
				coordinates.append("{},{}".format(x_cord,letters[index+t]))

	elif file.split(":")[1].split(";",1)[1] == "down;":  # if down
		index = int(start_coordinate.split(",")[0])

		if "Battleship" in ship_name:
			for t in range(4):
				coordinates.append("{},{}".format(index+t,y_cord))
		
		if "Patrol Boat" in ship_name:
			for t in range(2):
				coordinates.append("{},{}".format(index+t,y_cord))
		
	ships_dict[ship_name] = coordinates  # adding coordinates to ships dict


def create_battleships_and_patrol_boats(file):  # creating the battleship and patrol boats
	ships_dict={}
	for ship in file.split("\n"):
		optional_player(ship,ships_dict)  # using optional player function
	return ships_dict


def create_carrier_destroyer_submarine(dictionary,ships_dict):  # creating other ships
	ships_dict["Carrier"] = []
	ships_dict["Destroyer"] = []
	ships_dict["Submarine"] = []
	for row in dictionary:
		for char in dictionary[row]:
			if dictionary[row][char]=="C" and row != 0:
				ships_dict["Carrier"].append("{},{}".format(row,char))
			elif dictionary[row][char]=="D" and row != 0:
				ships_dict["Destroyer"].append("{},{}".format(row,char))
			elif dictionary[row][char]=="S" and row != 0:
				ships_dict["Submarine"].append("{},{}".format(row,char))


def check_for_ships(ship_name,board):  # checking how many ship is alive
	
	if board == player1_hidden_board: #  determining the player
		ships_dict = ships_dict1
	elif board == player2_hidden_board:
		ships_dict = ships_dict2
	
	if ship_name in "Carrier Destroyer Submarine":  # if the ship type has only one ship
		a = 0
		for cord in ships_dict[ship_name]:
			if board[int(cord.split(",")[0])][cord.split(",")[1]] == "X":
				a+=1
		if ship_name=="Carrier" and a ==5: # length 5
			return "X"
		elif ship_name=="Destroyer" and a ==3: # length 3
			return "X"
		elif ship_name=="Submarine" and a ==3: # length 3
			return "X"
		else:
			return "-"
	elif ship_name == "Battleship":  # for battleship which has 4 length and 2 ships
		a = 0
		for ship in ships_dict:
			if "Battleship" in ship:
				b = 0
				for cord in ships_dict[ship]:
					if board[int(cord.split(",")[0])][cord.split(",")[1]] == "X":
						b += 1
				if b ==4:
					a += 1
		if a == 0:
			return "- -"
		elif a == 1:
			return "X -"
		elif a == 2:
			return "X X"
	elif ship_name == "Patrol Boat":  # for patrol boat which has 2 length and 4 ships
		a = 0
		for ship in ships_dict:
			if "Patrol Boat" in ship:
				b=0
				for cord in ships_dict[ship]:
					if board[int(cord.split(",")[0])][cord.split(",")[1]] == "X":
						b += 1
				if b==2:
					a += 1
		if a == 0:
			return "- - - -"
		elif a == 1:
			return "X - - -"
		elif a == 2:
			return "X X - -"
		elif a == 3:
			return "X X X -"
		elif a == 4:
			return "X X X X"


# calling all the functions before running the main loop
file_read()
player1_board = create_board()
player2_board = create_board()
player1_hidden_board = create_board()
player2_hidden_board = create_board()
adding_input_to_the_board(player1_board,player1_ships)
adding_input_to_the_board(player2_board,player2_ships)
player1_shot_list = listing_the_shots(player1_in)
player2_shot_list = listing_the_shots(player2_in)
ships_dict1 = create_battleships_and_patrol_boats(optional_player1)
ships_dict2 = create_battleships_and_patrol_boats(optional_player2)
create_carrier_destroyer_submarine(player1_board,ships_dict1)
create_carrier_destroyer_submarine(player2_board,ships_dict2)


def print_ships():  # printing the ships function because we will use this several times // check for ships function is used in this function whic returns "X X - -"  vb.
	print_to_the_file_and_terminal("\nCarrier\t\t" + check_for_ships("Carrier",player1_hidden_board) + "\t\t\t\t" + "Carrier\t\t" + check_for_ships("Carrier",player2_hidden_board),"")
	print_to_the_file_and_terminal("Battleship\t" + check_for_ships("Battleship",player1_hidden_board) + "\t\t\t\t" + "Battleship\t" + check_for_ships("Battleship",player2_hidden_board),"")
	print_to_the_file_and_terminal("Destroyer\t" + check_for_ships("Destroyer",player1_hidden_board) + "\t\t\t\t" + "Destroyer\t" + check_for_ships("Destroyer",player2_hidden_board),"")
	print_to_the_file_and_terminal("Submarine\t" + check_for_ships("Submarine",player1_hidden_board) + "\t\t\t\t" + "Submarine\t" + check_for_ships("Submarine",player2_hidden_board),"")
	print_to_the_file_and_terminal("Patrol Boat\t" + check_for_ships("Patrol Boat",player1_hidden_board) + "\t\t\t" + "Patrol Boat\t" + check_for_ships("Patrol Boat",player2_hidden_board),"","")


def print_tables(board1,board2):  # printing the boards function beacuse we have 4 different board
	for i,row in enumerate(board1):
		row_string = ""
		for char in board1[row]:
			if board1[row][char] == 0:
				print_to_the_file_and_terminal(" "," "," ")
			elif board1[row][char] == 10:
				print_to_the_file_and_terminal(10," ","")
			else:
				print_to_the_file_and_terminal(board1[row][char]," "," ")
		print_to_the_file_and_terminal("\t\t"," ","")
		for char in board2[row]:
			if board2[row][char] == 0:
				print_to_the_file_and_terminal(" "," "," ")
			elif board2[row][char] == 10:
				print_to_the_file_and_terminal(10," ","")
			else:
				print_to_the_file_and_terminal(board2[row][char]," "," ")
		print_to_the_file_and_terminal("")

finish = False  # this variable for finishing the loop
count = 1 # this variable for determine the round
print_to_the_file_and_terminal("Battle of Ships Game\n") # big title

while not finish:

	# these two variable is for determining the winner with the help of check for ships variable
	is_player2_won = check_for_ships("Carrier",player1_hidden_board) + check_for_ships("Battleship",player1_hidden_board) + check_for_ships("Destroyer",player1_hidden_board) + check_for_ships("Submarine",player1_hidden_board) + check_for_ships("Patrol Boat",player1_hidden_board)
	is_player1_won = check_for_ships("Carrier",player2_hidden_board) + check_for_ships("Battleship",player2_hidden_board) + check_for_ships("Destroyer",player2_hidden_board) + check_for_ships("Submarine",player2_hidden_board) + check_for_ships("Patrol Boat",player2_hidden_board)
	
	if "-" not in is_player1_won:
		a = 0
		for row in player2_board:
			for char in player2_board[row]:
				if player2_board[row][char] not in "OX-":
					a +=1  # if there is a draw
					cord_row = row
					cord_char = char
		if a ==1 and player2_board[cord_row][cord_char]==player2_board[shot_list[(count)//2][0]][shot_list[(count)//2][1]]: # draw
			player2_board[cord_row][cord_char] == "X"
			player2_hidden_board[cord_row][cord_char] == "X"
			print_to_the_file_and_terminal("It is a Draw!\n\nFinal Information\n")
			print_to_the_file_and_terminal("Player1's Board\t\t\t\tPlayer2's Board")
			print_tables(player1_board,player2_board)
			print_ships()
		else: # player 1 wins
			player2_board[cord_row][cord_char] == "O"
			player2_hidden_board[cord_row][cord_char] == "O"
			print_to_the_file_and_terminal("Player1 Wins!\n\nFinal Information\n")
			print_to_the_file_and_terminal("Player1's Board\t\t\t\tPlayer2's Board")
			print_tables(player1_board,player2_board)
			print_ships()
		break
	elif "-" not in is_player2_won: # player 2 wins
		print_to_the_file_and_terminal("Player2 Wins!\n\nFinal Information\n")
		print_to_the_file_and_terminal("Player1's Board\t\t\t\tPlayer2's Board")
		print_tables(player1_hidden_board,player2_board)
		print_ships()
		break
	if count%2 == 1: # determining the round adnd the variables
		player = 1
		board = player2_board
		hidden_board = player2_hidden_board
		shot_list = player1_shot_list
	else:
		player = 2
		board = player1_board
		hidden_board = player1_hidden_board
		shot_list = player2_shot_list
	tittle_string = "Player{}'s Move\n\nRound : {}\t\t\t\t\tGrid Size: 10x10\n\nPlayer1's Hidden Board\t\tPlayer2's Hidden Board".format(player,(count+1)//2) # other title informations
	print_to_the_file_and_terminal(tittle_string)

	print_tables(player1_hidden_board,player2_hidden_board)
	print_ships()
	print_to_the_file_and_terminal("\n\nEnter your move: {},{}\n".format(shot_list[(count-1)//2][0],shot_list[(count-1)//2][1])) # print the move
	if board[int(shot_list[(count-1)//2][0])][shot_list[(count-1)//2][1]] not in "-O":  # changing the boards according to move
		hidden_board[int(shot_list[(count-1)//2][0])][shot_list[(count-1)//2][1]] = "X"
		board[int(shot_list[(count-1)//2][0])][shot_list[(count-1)//2][1]] = "X"
	else:
		hidden_board[int(shot_list[(count-1)//2][0])][shot_list[(count-1)//2][1]] = "O"
		board[int(shot_list[(count-1)//2][0])][shot_list[(count-1)//2][1]] = "O"

	if count%2 == 1:  # assigning the players board to changed board
		player2_hidden_board = hidden_board
	else:
		player1_hidden_board = hidden_board

	count += 1 # changing the round

# Ahmet Şeref Eker
# 2210356098
# Hacettepe University Computer Engineering