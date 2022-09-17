import org.json.simple.JSONObject;

import java.awt.*;
import java.io.File;
import java.net.http.HttpClient;
import java.util.List;

public class Controller {
    private ChessBoardPanel boardPanel;
    private HttpManager httpManager;

    public void addBoard(ChessBoardPanel boardPanel) {
        this.boardPanel = boardPanel;
        this.httpManager = new HttpManager("http", "localhost", 5000);
    }

    private boolean checkResponseStatus(JSONObject response) {
        if (response == null) {
            Utils.showError("Ошибка", "Проблема соединения");
            return false;
        }
        if (response.containsKey("status") && !((boolean) response.get(
                "status"))) {
            Utils.showError("Ошибка", (String) response.get("result"));
            return false;
        }
        return true;
    }

    public void createGame(String script, String playAs) {
        // called by `CreateGameWindow` when create button clicked. It takes
        // values from filled form fields and send request to server.
        JSONObject response = httpManager.loadScript(script);
        if (!checkResponseStatus(response)) {
            return;
        }
        JSONObject result = (JSONObject) response.get("result");
        response = httpManager.createGame((long) result.get("script_id"), playAs);
        if (checkResponseStatus(response)) {
            result = (JSONObject) response.get("result");
            new LinkWindow((String) result.get("link"));
        }
    }

    public void onCreateGameButton() {
        // show a form with field that user should fill. Disable tool buttons.
        new CreateGameWindow(this);
    }

    public void joinGame(String link) {
        JSONObject response = httpManager.joinGame(link);
        if (!checkResponseStatus(response)) {
            return;
        }
        GameState gameState = GameState.fromJSON((JSONObject) response.get("result"));
//        Color color = ((String) response.get("color")).equals("white") ? Color.WHITE : Color.BLACK;
        boardPanel.updateBoard(gameState, Color.WHITE, Color.WHITE);
    }

    public void onJoinGameButton() {
        // send request to join a game to server. If success,
        // `onMoveFromServer` will be called with appropriate game state.
        new JoinGameWindow(this);
    }

    public void onMoveByMouse(Point from, Point to) {
        // chess board panel has a set of possible moves, so we are guaranteed
        // to have a valid move here and only need to send it to server.
    }

    public void onMoveFromServer(List<Piece> pieces, List<Move> possibleMoves) {
        // receive game state (piece positions and possible moves) from a
        // server and update chess board panel with this data.
    }
}
