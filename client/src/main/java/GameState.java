import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

import java.util.ArrayList;

public class GameState {
    public final ArrayList<Piece> pieces;
    public final ArrayList<Move> possibleMoves;
    public final String status;

    public GameState(ArrayList<Piece> pieces, ArrayList<Move> possibleMoves, String status) {
        this.pieces = pieces;
        this.possibleMoves = possibleMoves;
        this.status = status;
    }

    public static GameState fromJSON(JSONObject json) {
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
        String status = (String) json.get("status");
        return new GameState(pieces, possibleMoves, status);
    }
}
