#static heuristic method
e_1 = [[120, -20,  20,   5,   5,  20, -20, 120],
    [-20, -40,  -5,  -5,  -5,  -5, -40, -20],
    [ 20,  -5,  15,   3,   3,  15,  -5,  20],
    [  5,  -5,   3,   3,   3,   3,  -5,   5],
    [  5,  -5,   3,   3,   3,   3,  -5,   5],
    [ 20,  -5,  15,   3,   3,  15,  -5,  20],
    [-20, -40,  -5,  -5,  -5,  -5, -40, -20],
    [120, -20,  20,   5,   5,  20, -20, 120]]
e_2 = [[100, -10, 11, 6, 6, 11, -10, 100], 
    [-10, -20, 1, 2, 2, 1, -20, -10], 
    [11, 1, 5, 4, 4, 5, 1, 11], 
    [6, 2, 4, 2, 2, 4, 2, 6], 
    [6, 2, 4, 2, 2, 4, 2, 6], 
    [11, 1, 5, 4, 4, 5, 1, 11], 
    [-10, -20, 1, 2, 2, 1, -20, -10], 
    [100, -10, 11, 6, 6, 11, -10, 100]]
# matrix e_2 works better then matrix e_1.    




#dynamic heuristic method
#pretty good can beat most of the AI
EMPTY = "."
BLACK = "X"
WHITE = "O"


class OthelloHeuristic(object):

    WIN = 1<<128
    PIECE_COUNT_FACTOR = [0, 0, 1]
    CORNER_FACTOR = [1000, 1000, 0]
    MOBILITY_FACTOR = [250, 300, 0]
    EDGE_FACTOR = [25, 25, 0]
    CORNER_EDGE_FACTOR = [400, 400, 0]
    STABILITY_FACTOR = [120, 120, 0]

    START_GAME = 0
    MID_GAME = 1
    END_GAME = 2

    def cal(self,board):
        cnt = 0
        for i in range(8):
            for j in range(8):
                if board._board[i][j] == EMPTY:
                    cnt += 1
        return cnt
    def evaluate(self, board, current_player, other_player):

        # Check for win conditions
        empty_spaces = self.cal(board)
        
        # Determine Game State to Determine Heuristic Values
        if empty_spaces >= 45:
            game_state = OthelloHeuristic.START_GAME
        elif empty_spaces >= 2:
            game_state = OthelloHeuristic.MID_GAME
        else:
            game_state = OthelloHeuristic.END_GAME

        score = 0
        if OthelloHeuristic.CORNER_FACTOR[game_state] != 0:
            score += self.evaluate_corner_pieces(board, current_player, other_player, game_state)
        if OthelloHeuristic.PIECE_COUNT_FACTOR[game_state] != 0:
            score += self.evaluate_piece_count(board, current_player, other_player, game_state)
        if OthelloHeuristic.MOBILITY_FACTOR[game_state] != 0:
            score += self.evaluate_mobility(board, current_player, other_player, game_state)
        if OthelloHeuristic.EDGE_FACTOR[game_state] != 0:
            score += self.evaluate_edge_pieces(board, current_player, other_player, game_state)
        if OthelloHeuristic.CORNER_EDGE_FACTOR[game_state] != 0:
            score += self.evaluate_corner_edge(board, current_player, other_player, game_state)
        if OthelloHeuristic.STABILITY_FACTOR[game_state] != 0:
            score += self.evaluate_stability(board, current_player, other_player, game_state)
        return score

    def evaluate_piece_count(self, board, current_player, other_player, game_state):
        score = 0
        if current_player == WHITE:
            score += OthelloHeuristic.PIECE_COUNT_FACTOR[game_state]*board.count(WHITE)
            score -= OthelloHeuristic.PIECE_COUNT_FACTOR[game_state]*board.count(BLACK)
        else:
            score += OthelloHeuristic.PIECE_COUNT_FACTOR[game_state]*board.count(BLACK)
            score -= OthelloHeuristic.PIECE_COUNT_FACTOR[game_state]*board.count(WHITE)
        return score

    def evaluate_corner_pieces(self, board, current_player, other_player, game_state):
        score = 0
        for i in [0, 7]:
            for j in [0, 7]:
                if board._board[i][j] == current_player:
                    score += OthelloHeuristic.CORNER_FACTOR[game_state]
                elif board._board[i][j] == other_player:
                    score -= OthelloHeuristic.CORNER_FACTOR[game_state]
        return score

    def evaluate_edge_pieces(self, board, current_player, other_player, game_state):
        score = 0
        # Compute Horizontal Edges
        for i in [0, 7]:
            for j in range(2, 6):
                if board._board[i][j] == current_player:
                    score += OthelloHeuristic.EDGE_FACTOR[game_state]
                elif board._board[i][j] == other_player:
                    score -= OthelloHeuristic.EDGE_FACTOR[game_state]
        # Comput Vertical Edges
        for i in range(2, 6):
            for j in [0, 7]:
                if board._board[i][j] == current_player:
                    score += OthelloHeuristic.EDGE_FACTOR[game_state]
                elif board._board[i][j] == other_player:
                    score -= OthelloHeuristic.EDGE_FACTOR[game_state]
        return score

    def evaluate_stability(self, board, current_player, other_player, game_state):
        score = 0
        corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
        for corner in corners:
            score += self.edge_stability(board, corner, current_player, game_state)
            score -= self.edge_stability(board, corner, other_player, game_state)
        return score

    def edge_stability(self, board, corner, current_player, game_state):
        score = 0
        if corner == (0, 0) and board._board[corner[0]][corner[1]] == current_player:
            score += OthelloHeuristic.STABILITY_FACTOR[game_state]
            i = 1
            while i < 7 and board._board[i][corner[1]] == current_player:
                score += OthelloHeuristic.STABILITY_FACTOR[game_state]
                i += 1
            i = 1
            while i < 7 and board._board[corner[0]][i] == current_player:
                score += OthelloHeuristic.STABILITY_FACTOR[game_state]
                i += 1
        elif corner == (0, 7) and board._board[corner[0]][corner[1]] == current_player:
            score += OthelloHeuristic.STABILITY_FACTOR[game_state]
            i = 1
            while i < 7 and board._board[i][corner[1]] == current_player:
                score += OthelloHeuristic.STABILITY_FACTOR[game_state]
                i += 1
            i = 6
            while i > 0 and board._board[corner[0]][i] == current_player:
                score += OthelloHeuristic.STABILITY_FACTOR[game_state]
                i -= 1
        elif corner == (7, 0) and board._board[corner[0]][corner[1]] == current_player:
            score += OthelloHeuristic.STABILITY_FACTOR[game_state]
            i = 6
            while i > 0 and board._board[i][corner[1]] == current_player:
                score += OthelloHeuristic.STABILITY_FACTOR[game_state]
                i -= 1
            i = 1
            while i < 7 and board._board[corner[0]][i] == current_player:
                score += OthelloHeuristic.STABILITY_FACTOR[game_state]
                i += 1
        elif corner == (7, 7) and board._board[corner[0]][corner[1]] == current_player:
            score += OthelloHeuristic.STABILITY_FACTOR[game_state]
            i = 6
            while i > 0 and board._board[i][corner[1]] == current_player:
                score += OthelloHeuristic.STABILITY_FACTOR[game_state]
                i -= 1
            i = 6
            while i > 0 and board._board[corner[0]][i] == current_player:
                score += OthelloHeuristic.STABILITY_FACTOR[game_state]
                i -= 1
        return score

    def evaluate_corner_edge(self, board, current_player, other_player, game_state):
        score = 0
        corner = (0, 0)
        for (i, j) in [(1, 0), (1, 1), (0, 1)]:
            if board._board[corner[0]][corner[1]] == EMPTY:
                if board._board[i][j] == current_player:
                    if i == 1 and j == 1:
                        score -= OthelloHeuristic.CORNER_EDGE_FACTOR[game_state]
                    else:
                        score -= OthelloHeuristic.CORNER_EDGE_FACTOR[game_state] / 2
                elif board._board[i][j] == other_player:
                    if i == 1 and j == 1:
                        score += OthelloHeuristic.CORNER_EDGE_FACTOR[game_state]
                    else:
                        score += OthelloHeuristic.CORNER_EDGE_FACTOR[game_state] / 2
        corner = (7, 0)
        for (i, j) in [(6, 0), (6, 1), (7, 1)]:
            if board._board[corner[0]][corner[1]] == EMPTY:
                if board._board[i][j] == current_player:
                    if i == 6 and j == 1:
                        score -= OthelloHeuristic.CORNER_EDGE_FACTOR[game_state]
                    else:
                        score -= OthelloHeuristic.CORNER_EDGE_FACTOR[game_state] / 2
                elif board._board[i][j] == other_player:
                    if i == 6 and j == 1:
                        score += OthelloHeuristic.CORNER_EDGE_FACTOR[game_state]
                    else:
                        score += OthelloHeuristic.CORNER_EDGE_FACTOR[game_state] / 2
        corner = (7, 7)
        for (i, j) in [(7, 6), (6, 6), (6, 7)]:
            if board._board[corner[0]][corner[1]] == EMPTY:
                if board._board[i][j] == current_player:
                    if i == 6 and j == 6:
                        score -= OthelloHeuristic.CORNER_EDGE_FACTOR[game_state]
                    else:
                        score -= OthelloHeuristic.CORNER_EDGE_FACTOR[game_state] / 2
                elif board._board[i][j] == other_player:
                    if i == 6 and j == 6:
                        score += OthelloHeuristic.CORNER_EDGE_FACTOR[game_state]
                    else:
                        score += OthelloHeuristic.CORNER_EDGE_FACTOR[game_state] / 2
        corner = (0, 7)
        for (i, j) in [(0, 6), (1, 6), (1, 7)]:
            if board._board[corner[0]][corner[1]] == EMPTY:
                if board._board[i][j] == current_player:
                    if i == 1 and j == 6:
                        score -= OthelloHeuristic.CORNER_EDGE_FACTOR[game_state]
                    else:
                        score -= OthelloHeuristic.CORNER_EDGE_FACTOR[game_state] / 2
                elif board._board[i][j] == other_player:
                    if i == 1 and j == 6:
                        score += OthelloHeuristic.CORNER_EDGE_FACTOR[game_state]
                    else:
                        score += OthelloHeuristic.CORNER_EDGE_FACTOR[game_state] / 2
        return score

    def evaluate_mobility(self, board, current_player, other_player, game_state):
        score = 0
        score += len(list(board.get_legal_actions(current_player)))*OthelloHeuristic.MOBILITY_FACTOR[game_state]
        score -= len(list(board.get_legal_actions(other_player)))*OthelloHeuristic.MOBILITY_FACTOR[game_state]
        return score

h = OthelloHeuristic()
class AIPlayer:
    """
    AI 玩家
    """
    def __init__(self, color):
        """
        玩家初始化
        :param color: 下棋方，'X' - 黑棋，'O' - 白棋
        """
        self.color = color
    
    def get_opponent(self,player):
        if player == "X":
            return "O"
        else:
            return "X"

    def heuristic(self,chess,player):
        return h.evaluate(chess,player,self.get_opponent(player))

    def AlphaBetaSearch(self,chess,depth,alpha,beta,player):
        if depth == 0:
            return self.heuristic(chess,player),None

        LegalMoveList = list(chess.get_legal_actions(player))
        if not LegalMoveList:
            return self.heuristic(chess,player),None

        if player == self.color:
            NextMove = None
            for Move in LegalMoveList: 
                flipped_pos = chess._move(Move, player)
                tmp,_ = self.AlphaBetaSearch(chess, depth-1, alpha, beta, self.get_opponent(player) )
                chess.backpropagation(Move, flipped_pos, player)
                if(tmp>alpha):
                    alpha = tmp
                    NextMove = Move
                if beta <= alpha: 
                    break                             
            return alpha,NextMove
        else:
            NextMove = None
            for Move in LegalMoveList: 
                flipped_pos = chess._move(Move, player)
                tmp,_ = self.AlphaBetaSearch(chess, depth-1, alpha, beta, self.get_opponent(player) )
                chess.backpropagation(Move, flipped_pos, player)
                if(tmp<beta):
                    beta = tmp
                    NextMove = Move
                if beta <= alpha: # 该极大节点的值<=beta<=alpha，该极小节点后面的搜索到的值肯定会小于α，因此不会被其上层的极大节点所选用了。对于根节点，α为负无穷
                    break                            
            return beta,NextMove

    def get_move(self, board):
        """
        根据当前棋盘状态获取最佳落子位置
        :param board: 棋盘
        :return: action 最佳落子位置, e.g. 'A1'
        """
        if self.color == 'X':
            player_name = '黑棋'
        else:
            player_name = '白棋'
        # print("请等一会，对方 {}-{} 正在思考中...".format(player_name, self.color))
        # -----------------请实现你的算法代码--------------------------------------
        depth = 4
        INF = 1<<128
        _, action = self.AlphaBetaSearch(board, depth, -INF, +INF, self.color)
        # _, action = self.minimax_alpha_beta(board, depth, -INF, +INF, self.color)
        # ------------------------------------------------------------------------
        return action
