import java.awt.Color;

public class Piece {
    public final String piece;
    public final Color color;
    public final String imageName;
    private int x;
    private int y;

    public Piece(String piece, Color color, int x, int y) {
        this.piece = piece;
        this.color = color;
        this.imageName = piece + (color == Color.WHITE ? "white" : "black");
        this.x = x;
        this.y = y;
    }

    public void move(int to_x, int to_y) {
        x = to_x;
        y = to_y;
    }

    public int getX() {return x;}

    public int getY() {return y;}

    @Override public int hashCode() {
        return 1000 * x + y;
    }

    @Override public boolean equals(Object other) {
        if (other == null) {
            return false;
        }
        if (!(other instanceof Piece otherPiece)) {
            return false;
        }
        return x == otherPiece.x && y == otherPiece.y;
    }
}