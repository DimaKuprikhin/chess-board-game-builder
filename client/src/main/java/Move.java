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

    @Override
    public String toString() {
        return "fromX: " + from.x + ", fromY: " + from.y + ", toX: " + to.x + ", toY: " + to.y;
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
        if (!(other instanceof Move otherMove)) {
            return false;
        }
        return from.x == otherMove.from.x && from.y == otherMove.from.y
                && to.x == otherMove.to.x && to.y == otherMove.to.y;
    }
}
