import static java.lang.Integer.max;
import static java.lang.Integer.min;

public class MiniMax {

    int isPreviousMoveFromLeft = 0;
    int isPreviousMoveFromRight = 0;

    Side mySide;

    public MiniMax(Side side){
        this.mySide = side;
    }

    int minimax(Kalah kalah_board, int alpha, int beta, Side side, int depth){
        Board board = kalah_board.getBoard();

        if (depth == 0 || kalah_board.gameOver()){
            return evalHeuristics(kalah_board.getBoard());
        }

        if (side == mySide) {
            int max_evaluation = - 9999;
            isPreviousMoveFromLeft = 1;

            for (int possible_move = 1; possible_move <= 7; possible_move++){
                Board board_copy = new Board(board);
                Kalah kalah_copy = new Kalah(board_copy);
                Move move = new Move(side, possible_move);
                if (kalah_copy.isLegalMove(move)){
                    isPreviousMoveFromRight = isMoveFromRightMostHole(board_copy, side, possible_move);
                    Side nextSide = kalah_copy.makeMove(move);
                    int evaluation = minimax(kalah_copy, alpha, beta, nextSide, depth - 1);
                    max_evaluation = max(max_evaluation, evaluation);
                    alpha = max(alpha, evaluation);
                    if (beta <= alpha)
                        break;
                    isPreviousMoveFromLeft = 0;
                }
            }
            return max_evaluation;
        }
        else {
            int min_evaluation = 9999;
            for (int possible_move = 1; possible_move <= 7; possible_move++){
                Board board_copy = new Board(board);
                Kalah kalah_copy = new Kalah(board_copy);
                Move move = new Move(side, possible_move);

                if (kalah_copy.isLegalMove(move)){
                    Side nextSide = kalah_copy.makeMove(move);
                    int evaluation = minimax(kalah_copy, alpha, beta, nextSide, depth - 1);
                    min_evaluation = min(min_evaluation, evaluation);
                    beta = min(beta, evaluation);
                    if (beta <= alpha)
                        break;
                }
            }
            return min_evaluation;
        }
    }


    int evalHeuristics(Board board){
        double w1 = 0.675;
        double w2 = 0.275;
        double w3 = 0.675;
        double w4 = 1.0;
        double w5 = 0.5;
        double w6 = 0.7;
        double w7 = 0.475;

        int h1 = hoardInLeftmostHole(board, mySide);
        int h2 = hoardOnMySide(board, mySide);
        int h3 = possibleMoves(board, mySide);
        int h4 = seedsInStore(board, mySide);
        int h5 = isPreviousMoveFromRight;
        int h6 = seedsInStore(board, mySide.opposite());
        int h7 = isPreviousMoveFromLeft;

        return (int)(h1 * w1 + h2 * w2 + h3 * w3 + h4 * w4 + h5 * w5 - h6 * w6 + h7 * w7);

    }

    int isMoveFromLeftMostHole(Board board, Side side, int move){
        int result = 0;

        for (int i = 1; i <= 7; i++){
            if (board.getSeeds(side, i) != 0){
                if (move == i)
                    result = 1;
                break;
            }
        }
        return result;
    }

    int seedsInStore(Board board, Side side){
        return board.getSeedsInStore(side);
    }

    int hoardInLeftmostHole(Board board, Side side){
        return board.getSeeds(side, 1);
    }

    int hoardOnMySide(Board board, Side side){
        int score = 0;

        for (int i = 1; i <= 7; i++){
            score += board.getSeeds(side, i);
        }

        return score;
    }

    int possibleMoves(Board board, Side side){
        int score = 0;

        for (int i = 1; i <= 7; i++){
            if (board.getSeeds(side, i) != 0)
                score += 1;
        }

        return score;
    }

    int isMoveFromRightMostHole(Board board, Side side, int move){
        int result = 0;

        for (int i = 7; i >= 1; i--){
            if (board.getSeeds(side, i) != 0){
                if (move == i)
                    result = 1;
                break;
            }
        }
        return result;
    }
}
