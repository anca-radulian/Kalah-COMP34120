import java.io.BufferedReader;
import java.io.EOFException;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.Reader;

/**
 * The main application class. It also provides methods for communication
 * with the game engine.
 */
public class Main
{
    /**
     * Input from the game engine.
     */
    private static Reader input = new BufferedReader(new InputStreamReader(System.in));

    /**
     * Sends a message to the game engine.
     * @param msg The message.
     */
    public static void sendMsg (String msg)
    {
        System.out.print(msg);
        System.out.flush();
    }

    /**
     * Receives a message from the game engine. Messages are terminated by
     * a '\n' character.
     * @return The message.
     * @throws IOException if there has been an I/O error.
     */
    public static String recvMsg() throws IOException
    {
        StringBuilder message = new StringBuilder();
        int newCharacter;

        do
        {
            newCharacter = input.read();
            if (newCharacter == -1)
                throw new EOFException("Input ended unexpectedly.");
            message.append((char)newCharacter);
        } while((char)newCharacter != '\n');

        return message.toString();
    }

    private static void makeBestMove(int hole) {
        sendMsg(Protocol.createMoveMsg(hole));
    }

    /**
     * The main method, invoked when the program is started.
     */
    public static void main(final String[] array) {
        try {
            final Board board = new Board(7, 7);
            int n = 1;
            while (true) {
                final String recvMsg = recvMsg();
                try {
                    switch (Protocol.getMessageType(recvMsg)) {
                        case START: {
                            final boolean interpretStartMsg = Protocol.interpretStartMsg(recvMsg);
                            Side.mySide = (interpretStartMsg ? Side.SOUTH : Side.NORTH);
                            if (interpretStartMsg) {
                                n = 0;
                                sendMsg(Protocol.createMoveMsg(2));
                                continue;
                            }
                            continue;
                        }
                        case STATE: {
                            final Protocol.MoveTurn interpretStateMsg = Protocol.interpretStateMsg(recvMsg, board);
                            if (interpretStateMsg.again && interpretStateMsg.move == -1) {
                                Side.mySide = Side.mySide.opposite();
                                // he swaped
                                int move = calculateNextBestMove(board, Side.mySide); // Stab
                                makeBestMove(move);
                            }
                            else if (interpretStateMsg.again && n != 0) {
                                if (interpretStateMsg.move <= 2) {
                                    // we swap
                                    Side.mySide = Side.mySide.opposite();
                                    sendMsg(Protocol.createSwapMsg());
                                }
                                else {
                                    int move = calculateNextBestMove(board, Side.mySide); // stab
                                    makeBestMove(move);
                                }
                            }
                            else if (interpretStateMsg.again) {
                                int move = calculateNextBestMove(board, Side.mySide); // Stab
                                makeBestMove(move);
                            }
//                            else {
//                                node = node.getChild(interpretStateMsg.move);
//                                node.addNewLayer();
//                            }
                            n = 0;
                            continue;
                        }
                        case END: {}
                    }
                }
                catch (InvalidMessageException ex) {
                    System.err.println(ex.getMessage());
                }
            }
        }
        catch (IOException ex2) {
            System.err.println("This shouldn't happen: " + ex2.getMessage());
        }
    }

    public static int calculateNextBestMove(Board board, Side side)
    {
        float [] scores = {-99999, -99999, -99999, -99999, -99999, -99999, -99999, -99999};
        float maxScore = -99999;
        int maxScoreIndex = 0;
        Kalah kalah = new Kalah(board);

        for (int i = 1; i <= 7; i++){
            Move move = new Move(side, i);
            if (kalah.isLegalMove(move)){
                Kalah newKalah = new Kalah(new Board(board));
               Side nextSide = newKalah.makeMove(move);
                scores[i] = new MiniMax(side).minimax(newKalah, -9999, 9999, nextSide, 11);
            }

            if (maxScore <= scores[i]){
                maxScoreIndex = i;
                maxScore = scores[i];
            }
        }

        return maxScoreIndex;
    }

    static {
        Main.input = new BufferedReader(new InputStreamReader(System.in));
    }
}
