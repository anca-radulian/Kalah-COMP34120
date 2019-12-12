/**
 * The side of the Kalah board a player can choose.
 */
public enum Side
{
    NORTH, SOUTH;

    public static Side mySide;

    /**
     * @return the side opposite to this one.
     */
    public Side opposite()
    {
        switch (this)
        {
            case NORTH: return SOUTH;
            case SOUTH: return NORTH;
            default: return NORTH;  // dummy
        }
    }

    public static boolean myTurn(final Side side) {
        return side == Side.mySide;
    }

    static {
        Side.mySide = Side.SOUTH;
    }
}