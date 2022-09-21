import org.json.simple.JSONObject;

import java.awt.*;

public class Move {
    public final Point from;
    public final Point to;

    Move(Point from, Point to) {
        this.from = from;
        this.to = to;
    }

    public static Move fromJSON(JSONObject json) {
        final int fromX = ((Long) json.get("from_x")).intValue();
        final int fromY = ((Long) json.get("from_y")).intValue();
        final int toX = ((Long) json.get("to_x")).intValue();
        final int toY = ((Long) json.get("to_y")).intValue();
        return new Move(new Point(fromX, fromY), new Point(toX, toY));
    }

    public JSONObject toJSON() {
        JSONObject move = new JSONObject();
        move.put("from_x", from.x);
        move.put("from_y", from.y);
        move.put("to_x", to.x);
        move.put("to_y", to.y);
        return move;
    }

    @Override
    public String toString() {
        return "{ \"from_x\": " + from.x + ", \"from_y\": " + from.y + ", \"to_x\": " + to.x + ", \"to_y\": " + to.y + " }";
    }

    @Override
    public int hashCode() {
        return 1000 * from.x + 100 * from.y + 10 * to.x + to.y;
    }

    @Override
    public boolean equals(Object other) {
        if (other == null) {
            return false;
        }
        if (!(other instanceof Move)) {
            return false;
        }
        Move otherMove = (Move) other;
        return from.x == otherMove.from.x && from.y == otherMove.from.y
                && to.x == otherMove.to.x && to.y == otherMove.to.y;
    }
}
