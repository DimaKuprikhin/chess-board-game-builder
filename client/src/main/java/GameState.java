import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

import java.util.ArrayList;

public class GameState {
    public final ArrayList<Piece> pieces;
    public final ArrayList<Move> possibleMoves;

    public GameState(ArrayList<Piece> pieces, ArrayList<Move> possibleMoves) {
        this.pieces = pieces;
        this.possibleMoves = possibleMoves;
    }

    public static GameState fromJSON(JSONObject json) {
        System.out.println(json.toJSONString());
        Object[] piecesJson = ((JSONArray) json.get("pieces")).toArray();
        Object[] possibleMovesJson = ((JSONArray) json.get("possible_moves")).toArray();
        ArrayList<Piece> pieces = new ArrayList<>();
        ArrayList<Move> possibleMoves = new ArrayList<>();
        for (Object piece : piecesJson) {
            pieces.add(Piece.fromJSON((JSONObject) piece));
        }
        for (Object move : possibleMovesJson) {
            possibleMoves.add(Move.fromJSON((JSONObject) move));
        }
        return new GameState(pieces, possibleMoves);
    }
}
