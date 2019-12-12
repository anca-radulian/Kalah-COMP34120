import static java.lang.Float.max;
import static java.lang.Float.min;

public class MiniMax {

    int isPreviousMoveFromLeft = 0;
    int isPreviousMoveFromRight = 0;

    Side mySide;

    public MiniMax(Side side){
        this.mySide = side;
    }

    float minimax(Kalah kalah_board, float alpha, float beta, Side side, int depth){
        Board board = kalah_board.getBoard();

        if (depth == 0 || kalah_board.gameOver()){
                return evalHeuristics(kalah_board.getBoard());
        }

        if (side == mySide) {
            float max_evaluation = - 9999;
            isPreviousMoveFromLeft = 1;

            for (int possible_move = 1; possible_move <= 7; possible_move++){
                Board board_copy = new Board(board);
                Kalah kalah_copy = new Kalah(board_copy);
                Move move = new Move(side, possible_move);
                if (kalah_copy.isLegalMove(move)){
                    isPreviousMoveFromRight = isMoveFromRightMostHole(board_copy, side, possible_move);
                    Side nextSide = kalah_copy.makeMove(move);
                    float evaluation = minimax(kalah_copy, alpha, beta, nextSide, depth - 1);
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
            float min_evaluation = 9999;
            for (int possible_move = 1; possible_move <= 7; possible_move++){
                Board board_copy = new Board(board);
                Kalah kalah_copy = new Kalah(board_copy);
                Move move = new Move(side, possible_move);

                if (kalah_copy.isLegalMove(move)){
                    Side nextSide = kalah_copy.makeMove(move);
                    float evaluation = minimax(kalah_copy, alpha, beta, nextSide, depth - 1);
                    min_evaluation = min(min_evaluation, evaluation);
                    beta = min(beta, evaluation);
                    if (beta <= alpha)
                        break;
                }
            }
            return min_evaluation;
        }
    }


    float evalHeuristics(Board board){
        float w1 = 1.0f;
        float w2 = 0.309f;
        float w3 = 0.404f;
        float w4 = 0.761f;
        float w5 = 0.285f;
        float w6 =  0.738f;

        float h1 = hoardInLeftmostHole(board, mySide);
        float h2 = hoardOnMySide(board, mySide);
        float h3 = possibleMoves(board, mySide);
        float h4 = seedsInStore(board, mySide);
        float h5 = isPreviousMoveFromRight;
        float h6 = seedsInStore(board, mySide.opposite());

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
