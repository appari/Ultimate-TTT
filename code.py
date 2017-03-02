import numpy
possible_wins = ([[(0,0),(0,1),(0,2),(0,3)],
				[(1,1),(1,2),(1,3),(1,0)],
				[(2,1),(2,2),(2,3),(2,0)],
				[(3,1),(3,2),(3,3),(3,0)],
				[(1,0),(2,0),(3,0),(0,0)],
				[(1,1),(2,1),(3,1),(0,1)],
				[(1,2),(2,2),(3,2),(0,2)],
				[(1,3),(2,3),(3,3),(0,3)],
				[(0,0),(1,1),(2,2),(3,3)],
				[(3,0),(2,1),(1,2),(0,3)],
				]) 
value_arr = ([[0, -10,-50,-100,-500],[10, 0,0,0],[50,0,0,0],[100,0,0,0],[500,0,0,0]])
block_vals = [[0 for x in range(4)] for y in range(4)] 
final_block = [[0 for x in range(4)] for y in range(4)] 

class My_Player():
	def __init__(self):
		self.cn=0
		pass
	def min(self,a,b):
		if(a<=b):
			return a
		else:
			return b
	def max(self,a,b):
		if(a>=b):
			return a
		else:
			return b
	def move(self, board, old_move, flag):
		print "Old Move:" , old_move
		self.cn=0
		value,next_move = self.minimax(old_move, False, -1000,1000,board)
		return next_move

	def evaluate(self,board,maximizingPlayer,old_move):		
		block_vals = final_block
		if(maximizingPlayer):
			Me = 'x'
			Opp = 'o'
		else:
			Me = 'o'
			Opp = 'x'
		val = 0
		finalval =0 
		myblock = [old_move[0]//4, old_move[1]//4]	
		tmp1 = 4*myblock[0]
		tmp2 = 4*myblock[1]
		for i in xrange(10):
			players=0
			others=0
			for j in xrange(4):
				piece = board.board_status[tmp1+possible_wins[i][j][0]][tmp2+possible_wins[i][j][1]]
				if(piece == Me):
					players += 1
				elif(piece == Opp):
					others += 1
			val += value_arr[players][others]

		block_vals[myblock[0]][myblock[1]] = val
		for i in xrange(10):
			players=0
			others=0
			for j in xrange(4):
				piece = board.block_status[possible_wins[i][j][0]][possible_wins[i][j][1]]
				if(piece == Me):
					players += 1
				elif(piece == Opp):
					others += 1
			try:
				finalval += block_vals[players][others]
			except Exception as e:
				print e
		return finalval

	def minimax(self,old_move, maximizingPlayer, alpha, beta,board):
		if(maximizingPlayer):
			flag = 'x'
			best=-1000
		else:
			flag = 'o'
			best=1000
		hvalue	= self.check_win(board,flag)
	#	print "Hvalue:",hvalue

		if(hvalue == 'o'):
			return 100,None
			final_block[old_move[0]//4][old_move[1]//4] == score
		elif(hvalue == 'x'):
			return -100 , None
			final_block[old_move[0]//4][old_move[1]//4] == score
		elif(hvalue == 'NONE'):
			return 0, None
			final_block[old_move[0]//4][old_move[1]//4] == score
		score = self.evaluate(board,maximizingPlayer,old_move)
		#print "Score:" , score
		cells = board.find_valid_move_cells(old_move)	
	#	print "Valid moves:",cells
		best_move = None
		for mycell in cells:
			#print "Mycell:",mycell
			myblock = [mycell[0]//4, mycell[1]//4]	
	#		print myblock
			board.board_status[mycell[0]][mycell[1]] = flag

			winlose = self.check_block(board,flag,myblock)
		#	print "Winlose:", winlose
			if(winlose):
				board.block_status[myblock[0]][myblock[1]] = flag
			if(maximizingPlayer):
				val, new_move = self.minimax(mycell, False ,alpha,beta,board)
				board.board_status[mycell[0]][mycell[1]] = '-'
				board.block_status[myblock[0]][myblock[1]] = '-'
				if best < val:
					best = val
					best_move=mycell
				alpha = self.max(alpha,best)
				if(beta<=alpha):
					break
			else:
				val, new_move = self.minimax(mycell,True ,alpha,beta,board)
				board.board_status[mycell[0]][mycell[1]] = '-'
				board.block_status[myblock[0]][myblock[1]] = '-'
				if best > val:
					best = val
					best_move=mycell
		#		print best
		#		print best_move
				beta = self.min(beta,best)
				if(beta<=alpha):
					break
		return score,best_move
		


	def check_win(self,board,flag):
		self.cn+=1
		if self.cn>2:
			return 'o'
		whowonorlost = board.find_terminal_state()
		return whowonorlost[0]

	def check_block(self,board,flag,myblock):
		bs = board.board_status
		a = 4*myblock[0]
		b = 4*myblock[1]

		#diagonals
		if(bs[a][b] ==  bs[a+1][b+1] == bs[a+2][b+2] ==bs[a+3][b+3] == flag):
			return True
		elif(bs[a][b+3] == bs[a+1][b+2] == bs[a+2][b+1] ==bs[a+3][b] == flag):
			return True
		
		#columns
		elif(bs[a][b] == bs[a][b+1] == bs[a][b+2] ==bs[a][b+3] == flag):
			return True
		elif(bs[a+1][b] == bs[a+1][b+1] == bs[a+1][b+2] ==bs[a+1][b+3] == flag):
			return True
		elif(bs[a+2][b] == bs[a+2][b+1] == bs[a+2][b+2] ==bs[a+2][b+3] == flag):
			return True
		elif(bs[a+3][b] == bs[a+3][b+1] == bs[a+3][b+2] ==bs[a+3][b+3] == flag):
			return True

		#rows
		elif(bs[a][b] == bs[a+1][b] == bs[a+2][b] ==bs[a+3][b] == flag):
			return True
		elif(bs[a][b+1] == bs[a+1][b+1] == bs[a+2][b+1] ==bs[a+3][b+1] == flag):
			return True
		elif(bs[a][b+2] == bs[a+1][b+2] == bs[a+2][b+2] ==bs[a+3][b+2] == flag):
			return True
		elif(bs[a][b+3] == bs[a+1][b+3] == bs[a+2][b+3] ==bs[a+3][b+3] == flag):
			return True
		
		return False