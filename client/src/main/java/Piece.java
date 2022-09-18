import org.json.simple.JSONObject;

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

    public static Piece fromJSON(JSONObject json) {
        final String name = (String) json.get("name");
        final Color color = Utils.fromString((String) json.get("color"));
        final int x = ((Long) json.get("x")).intValue();
        final int y = ((Long) json.get("y")).intValue();
        return new Piece(name, color, x, y);
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
        if (!(other instanceof Piece)) {
            return false;
        }
        Piece otherPiece = (Piece) other;
        return x == otherPiece.x && y == otherPiece.y;
    }
}
