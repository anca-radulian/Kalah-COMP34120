import static java.lang.Double.max;
import static java.lang.Double.min;

public class MiniMax {

    int isPreviousMoveFromRight = 0;

    Side mySide;

    public MiniMax(Side side){
        this.mySide = side;
    }

    double minimax(Kalah kalah_board, double alpha, double beta, Side side, int depth){
        Board board = kalah_board.getBoard();

        if (depth == 0 || kalah_board.gameOver()){
            return evalHeuristics(kalah_board.getBoard());
        }

        if (side == mySide) {
            double max_evaluation = - 9999;

            for (int possible_move = 1; possible_move <= 7; possible_move++){
                Board board_copy = new Board(board);
                Kalah kalah_copy = new Kalah(board_copy);
                Move move = new Move(side, possible_move);
                if (kalah_copy.isLegalMove(move)){
                    isPreviousMoveFromRight = isMoveFromRightMostHole(board_copy, side, possible_move);
                    Side nextSide = kalah_copy.makeMove(move);
                    double evaluation = minimax(kalah_copy, alpha, beta, nextSide, depth - 1);
                    max_evaluation = max(max_evaluation, evaluation);
                    alpha = max(alpha, evaluation);
                    if (beta <= alpha)
                        break;
                }
            }
            return max_evaluation;
        }
        else {
            double min_evaluation = 9999;
            for (int possible_move = 1; possible_move <= 7; possible_move++){
                Board board_copy = new Board(board);
                Kalah kalah_copy = new Kalah(board_copy);
                Move move = new Move(side, possible_move);

                if (kalah_copy.isLegalMove(move)){
                    Side nextSide = kalah_copy.makeMove(move);
                    double evaluation = minimax(kalah_copy, alpha, beta, nextSide, depth - 1);
                    min_evaluation = min(min_evaluation, evaluation);
                    beta = min(beta, evaluation);
                    if (beta <= alpha)
                        break;
                }
            }
            return min_evaluation;
        }
    }


    double evalHeuristics(Board board){
        double w1 = 0.198649;
        double w2 = 0.190084;
        double w3 = 0.370793;
        double w4 = 1;
        double w5 = 0.418841;
        double w6 = 0.565937;

        double h1 = hoardInLeftmostHole(board, mySide);
        double h2 = hoardOnMySide(board, mySide);
        double h3 = possibleMoves(board, mySide);
        double h4 = seedsInStore(board, mySide);
        double h5 = isPreviousMoveFromRight;
        double h6 = seedsInStore(board, mySide.opposite());

        return h1 * w1 + h2 * w2 + h3 * w3 + h4 * w4 + h5 * w5 - h6 * w6;
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