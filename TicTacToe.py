# By J. A. Mendez @jam65st
# IMPORTS
from random import randint

# CONSTANTS
MACHINE = 'Machine'
PLAYER = 'Player'
BOX = 3
WBOARD = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]
BBOARD = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

# Messages
CLEAN = '|' + ' ' * 23 + '|'
EMPTY = '*' + '-' * 24 + '*'
INTRO = EMPTY + '\n| My Tic Tac Toe ' + ' ' * 8 + '|\n' + EMPTY
INIT = '| Are you ready to play? |'
START = '|' + ' ' * 4 + '-> Press Y to Start '
AGAIN = '|' + ' ' * 11 + 'Play again? |'
RETRY = '| Y Continue | X to Exit |'
EXIT = EMPTY + '\n|' + ' ' * 5 + 'G O O D  B Y E' + ' ' * 5 + '|\n' + EMPTY
URMOVE = '| Enter your move: '
TYPERR = '|\n|>Numbers between 1 to 9<|'
BUSYER = '|\n| ¡¡¡You was selected a busy cell!!! |'

BOXTOP = '+' + '-' * 7 + '+' + '-' * 7 + '+' + '-' * 7 + '+'
BOXMID = '|' + ' ' * 7 + '|' + ' ' * 7 + '|' + ' ' * 7 + '|'
BOXSET = BOXTOP + '\n' + BOXMID + '\n'

# VARIABLES
board = []
empty = []
options = []
current = MACHINE
plays = 0

# settings
settings = {
	'is_fixed': True,
	'default_figure': 'X',
	'init_at_center': True
}
''' settings
	contains app parameters such as:
	- is_fixed: Game can use random figures (False) or fixed (True)
	- default_figure: If fixed, then only will used this character for MACHINE
	- init_at_center: The MACHINE always start in the middle of the board
'''


# METHODS
def greeting(firstTime=False):
	# Initial Message
	if firstTime == True: print(INTRO)
	
	# Game greeting
	print(INIT if firstTime else AGAIN)
	
	# User Interaction
	start = input(START if firstTime else RETRY)
	if start.lower() != 'x' and start.lower() != 'y':
		print(EMPTY)
		greeting()
	if start.lower() == 'x':
		print(EXIT)
		exit()
	
	# Reset
	global board, empty, figure, options, plays
	board, empty = initNewBoard(), BBOARD.copy()
	options = empty.copy()
	figure = chooseInit() if settings['is_fixed'] == False else settings['default_figure']
	plays = 0
	current = MACHINE
	
	addMove(1)


def addMove(n=0):
	if current == MACHINE:
		move = 5 if settings['init_at_center'] == True and plays == 0 else chooseNewMachineOption()  # assign a number
		fig = figure
		validateMove(move, fig)
	else:
		try:
			move = int(input(URMOVE))
			# Validate value
			fig = "O" if figure == 'X' else 'X'
			validateMove(move, fig)
		except TypeError:
			print(TYPERR + '\tTYPE')
			addMove(-1)
		except ValueError:
			print(TYPERR + '\tVALUE')
			addMove(-2)


def validateMove(move, fig):
	if empty[move - 1] != 'X' and empty[move - 1] != 'O':
		showMove(move, fig)
	else:
		if current == PLAYER: print(BUSYER)
		addMove(-3)


def initNewBoard(): return WBOARD.copy()


def chooseInit():
	min = randint(0, 500)
	max = randint(min, 1000)
	return 'X' if randint(min // 2, max // 2) % 2 == 0 else 'O'


def showMove(move, fig):
	global plays, board, current, options
	print(f'{CLEAN}\n| {plays + 1}) {current} Move:\t{move} | {fig}')
	for i in range(BOX):
		line = ''
		for j in range(BOX):
			p = (i * 3) + j
			if move == p + 1:
				board[i][j] = fig
				empty[p] = fig
				options.remove(str(move))
			line += '|' + ' ' * 3 + board[i][j] + ' ' * 3
		line += '|'
		print(BOXSET + line + '\n' + BOXMID)
	print(BOXTOP)  # + '-' * 12 + '*')
	plays += 1
	# swap player
	current = PLAYER if current == MACHINE else MACHINE
	testWinner()


def chooseNewMachineOption():
	min = randint(0, 500)
	max = randint(min, 1000)
	opts = len(options)
	result = randint(min, max) % opts
	return result if result > 0 and result < opts + 1 else chooseNewMachineOption()


def testWinner():
	if (plays < BOX):
		addMove(2)
	else:
		test = checkBoard()
		if len(test) == 0 and len(options) == 0:
			print('| There is NO WINNER!!!\n   |')
			greeting(False)
		elif len(test) == 0 and len(options) > 0:
			addMove(3)
		else:
			printWinnerBoard(test)


def checkBoard():
	# check horizontal board
	if empty[0] == empty[1] and empty[1] == empty[2]: return [0, 1, 2]
	if empty[3] == empty[4] and empty[4] == empty[5]: return [3, 4, 5]
	if empty[6] == empty[7] and empty[7] == empty[8]: return [6, 7, 8]
	# check vertical board
	if empty[0] == empty[3] and empty[3] == empty[6]: return [0, 3, 6]
	if empty[1] == empty[4] and empty[4] == empty[7]: return [1, 4, 7]
	if empty[2] == empty[5] and empty[5] == empty[8]: return [2, 5, 8]
	# check diagonals board
	if empty[0] == empty[4] and empty[4] == empty[8]: return [0, 5, 8]
	if empty[6] == empty[4] and empty[4] == empty[2]: return [0, 5, 8]
	return []


def printWinnerBoard(winnerCells):
	print(f'| {MACHINE if current == PLAYER else PLAYER } Wins!!!\t    |')
	for i in range(BOX):
		mids = '\n'
		line = '\n'
		for j in range(BOX):
			p = (i * 3) + j
			fill = '*' if p in winnerCells else ' '
			mids += '|' + fill * 7
			line += '|' + fill * 3 + board[i][j] + fill * 3
		mids += '|'
		line += '|'
		print(BOXTOP + mids + line + mids)
	print(BOXTOP)
	greeting(False)


greeting(True)
