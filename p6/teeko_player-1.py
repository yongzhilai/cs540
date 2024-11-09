import random
import copy
import math

class TeekoPlayer:
    """ An object representation for an AI game player for the game Teeko.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']

    def __init__(self):
        """ Initializes a TeekoPlayer object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]
        
    def succ(self,state,turn):
        count=0
        drop_phase= False
        for i in range(5):
            for j in range(5):
                if state[i][j]!=' ':
                    count=count+1
        if count<8:
            drop_phase =  True
        if drop_phase==True:
            return self.drop_succ(state,turn)
        if drop_phase==False:
            return self.normal_succ(state,turn)
    def drop_succ(self,state, turn):
        successor_list=[]
        COPY=copy.deepcopy(state)
        for r in range(5):
            for i in range(5):
                if COPY[r][i]==' ':
                    COPY[r][i]=turn
                    successor_list.append(COPY)
                COPY=copy.deepcopy(state)
        return successor_list
                    
    def normal_succ(self,state, turn):
        #Args: state the current state
        #turn: whose turn it is, a color between r and b
        successor_list=[]
        COPY=copy.deepcopy(state)
        print('y')
        for r in range(5):
            for i in range(5):
                if COPY[r][i]==turn:
                    for x in range(5):
                        if COPY[r][x]==' 'and abs(x-i)==1:
                            COPY[r][x]=turn
                            COPY[r][i]=' '
                            successor_list.append(COPY)
                        COPY=copy.deepcopy(state)
                    for j in range(5):
                        if COPY[j][i]==' 'and abs(j-r)==1:
                            COPY[j][i]=turn
                            COPY[r][i]=' '
                            successor_list.append(COPY)
                        COPY=copy.deepcopy(state)
                    for g in range(5):
                        for k in range(5):
                            if COPY[g][k]==' ' and g+k==r+i and abs(g-r)==1:
                                COPY[g][k]=turn
                                COPY[r][i]=' '
                                successor_list.append(COPY)
                            COPY=copy.deepcopy(state)
                    for g in range(5):
                        for k in range(5):
                            if COPY[g][k]==' ' and g-k==r-i and abs(g-r)==1:
                                COPY[g][k]=turn
                                COPY[r][i]=' '
                                successor_list.append(COPY)
                            COPY=copy.deepcopy(state)
                            
        
        return successor_list
    
    def make_move(self, state):
        """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.
            
        Args:
            state (list of lists): should be the current state of the game as saved in
                this TeekoPlayer object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.
                
                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).
        
        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.
        """
          # TODO: detect drop phase
        move = []
        opt_coord=[]
        state_coord=[]
        trace=self.Max_Value(state,2)[1]
        opt_state=trace[len(trace)-2]
        for i in range(5):
            for j in range(5):
                if opt_state[i][j]==self.my_piece:
                    opt_coord.append((i,j))
        for i in range(5):
            for j in range(5):
                if state[i][j]==self.my_piece:
                    state_coord.append((i,j))
                    
        set1=set(opt_coord)
        set2=set(state_coord)
        set3=set1-set2#new coord
        set4=set2-set1#old coord
        count=0
        drop_phase= False
        for i in range(5):
            for j in range(5):
                if state[i][j]!=' ':
                    count=count+1
        if count<8:
            drop_phase =  True
        if drop_phase==True:
            move.append(set3.pop())
            
        if drop_phase==False:
            move.append(set3.pop())
            move.append(set4.pop())
            
        # select an unoccupied space randomly
        # TODO: implement a minimax algorithm to play better
        
        return move
    
    def Max_Value(self,state,depth):
        result=self.game_value(state)
        trace=[]
        if result==1 or result==-1:
            trace.append(state)
            return (result,trace)
        elif depth==0:
            trace.append(state)
            return (self.heuristic_game_value(state),trace)
        else:
            max_tup=(-100,[])
            for x in self.succ(state,self.my_piece):
                cur=self.Min_Value(x,depth-1)
                if cur[0]>max_tup[0]:
                    max_tup=cur
            max_tup[1].append(state)
            return max_tup
        
    def Min_Value(self,state,depth):
        result=self.game_value(state)
        trace=[]
        if result==1 or result==-1:
            trace.append(state)
            return (result,trace)
        elif depth==0:
            trace.append(state)
            return (self.heuristic_game_value(state),trace)
        else:
            min_tup=(100,[])
            for x in self.succ(state,self.opp):
                cur=self.Max_Value(x,depth-1)
                if cur[0]<min_tup[0]:
                    min_tup=cur
            min_tup[1].append(state)
            return min_tup

    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                raise Exception("You don't have a piece there!")
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)
        
    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece
        
        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
                
                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece
        
    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row)+": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")
        
    def game_value(self, state):
        """ Checks the current board status for a win condition
        
        Args:
        state (list of lists): either the current state of the game as saved in
            this TeekoPlayer object, or a generated successor state.

        Returns:
            int: 1 if this TeekoPlayer wins, -1 if the opponent wins, 0 if no winner

        TODO: complete checks for diagonal and 2x2 box wins
        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i+1] == row[i+2] == row[i+3]:
                    return 1 if row[i]==self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i+1][col] == state[i+2][col] == state[i+3][col]:
                    return 1 if state[i][col]==self.my_piece else -1

        # TODO: check \ diagonal wins
        if state[3][0] !=' ' and state[3][0]==state[2][1]==state[1][2]==state[0][3]:
            return 1 if state[3][0]==self.my_piece else -1
        if state[4][1] !=' ' and state[4][1]==state[3][2]==state[2][3]==state[1][4]:
            return 1 if state[4][1]==self.my_piece else -1
        if state[4][0] !=' ' and state[4][0]==state[4-1][0+1]==state[4-2][0+2]==state[4-3][0+3]:
            return 1 if state[4][0]==self.my_piece else -1
        if state[3][1] !=' ' and state[3][1]==state[2][2]==state[1][3]==state[0][4]:
            return 1 if state[3][1]==self.my_piece else -1
        # TODO: check / diagonal wins
        if state[1][0] !=' ' and state[1][0]==state[2][1]==state[3][2]==state[4][3]:
            return 1 if state[1][0]==self.my_piece else -1
        if state[0][1] !=' ' and state[0][1]==state[1][2]==state[2][3]==state[3][4]:
            return 1 if state[0][1]==self.my_piece else -1
        if state[0][0] !=' ' and state[0][0]==state[1][1]==state[2][2]==state[3][3]:
            return 1 if state[0][0]==self.my_piece else -1
        if state[1][1] !=' ' and state[1][1]==state[2][2]==state[3][3]==state[4][4]:
            return 1 if state[1][1]==self.my_piece else -1
        # TODO: check 2x2 box wins
        
        for r in range(4):
            for i in range(4):
                if state[r][i] != ' ' and state[r][i]==state[r][i+1]==state[r+1][i]==state[r+1][i+1]:
                    return 1 if state[r][i]==self.my_piece else -1
        
        return 0 # no winner yet
    
    def heuristic_game_value(self,state):
        result=self.game_value(state)
        if result==1 or result==-1:
            return result
        max_count=0
        
        for i in range(5):          
            for j in range(5):
                if state[i][j]==self.my_piece:
                    count=0
                    neighbors=self.nearby_coord((i,j))
                    for x in neighbors:
                        if state[x[0]][x[1]]==self.my_piece:
                            count=count+1
                    if count>max_count:
                        max_count=count
        if max_count==0:
            return 0
        elif max_count==1:
            return 0.2
        elif max_count==2:
            return 0.4
        else:
            return 0.6
    
    def nearby_coord(self, coord:tuple):
        (x, y) = coord

        possible_coords = [(x+1, y+1), (x+1, y-1), (x+1, y), (x-1, y+1), (x-1, y-1), (x-1, y), (x, y+1), (x, y-1)]
        coords = []

        for x in possible_coords:
            (x1, y1) = x

            if 0 <= x1 < 5 and 0 <= y1 < 5:
                coords.append(x)

        return coords


