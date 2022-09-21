import org.json.simple.JSONObject;

import java.awt.*;
import java.util.ArrayList;
import java.util.Timer;
import java.util.TimerTask;

public class Controller {

    private ChessBoardPanel boardPanel;
    private HttpManager httpManager;
    private Long gameId = null;
    private Timer timer = new Timer();
    private LinkWindow linkWindow = null;

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
            Utils.showError("Ошибка", "Ошибкана сервере");
            return false;
        }
        return true;
    }

    private void scheduleUpdateGameState() {
        if (timer == null) {
            timer = new Timer();
        }
        long TIMER_TASK_DELAY = 2000;
        timer.schedule(new TimerTask() {
            @Override public void run() {
                updateGameState();
            }
        }, TIMER_TASK_DELAY);
    }

    private void cancelTimer() {
        timer.cancel();
        timer = null;
    }

    private boolean handleGameEnding(GameState gameState) {
        String message = null;
        if (gameState.status.equals("draw")) {
            message = "Ничья!";
        }
        if (gameState.status.equals("white won")) {
            message = "Белые победили!";
        }
        if (gameState.status.equals("black won")) {
            message = "Черные победили!";
        }
        if (message != null) {
            Utils.showInfo("Игра закончена", message);
            return true;
        }
        return false;
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
            gameId = (Long) result.get("id");
            linkWindow = new LinkWindow((String) result.get("link"));
            scheduleUpdateGameState();
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
        JSONObject result = (JSONObject) response.get("result");
        GameState gameState = GameState.fromJSON((JSONObject) result.get("game_state"));
        Color color = Utils.fromString((String) result.get("color"));
        Color turn = Utils.fromString((String) result.get("turn"));
        this.gameId = (Long) result.get("game_id");
        boardPanel.updateBoard(gameState, color, turn);
        if (color != turn) {
            scheduleUpdateGameState();
        }
    }

    public void onJoinGameButton() {
        // send request to join a game to server. If success,
        // `onMoveFromServer` will be called with appropriate game state.
        new JoinGameWindow(this);
    }

    private void updateGameState() {
        JSONObject response = httpManager.getGameState(gameId);
        if (!checkResponseStatus(response)) {
            return;
        }
        JSONObject result = (JSONObject) response.get("result");
        GameState gameState = GameState.fromJSON((JSONObject) result.get("game_state"));
        Color color = Utils.fromString((String) result.get("color"));
        Color turn = Utils.fromString((String) result.get("turn"));
        if (handleGameEnding(gameState)) {
            cancelTimer();
            boardPanel.updateBoard(
                    new GameState(gameState.pieces, new ArrayList<>(), gameState.status), color, turn);
            return;
        }
        boardPanel.updateBoard(gameState, color, turn);
        if (!gameState.status.equals("not started")) {
            if (linkWindow != null) {
                linkWindow.dispose();
                linkWindow = null;
            }
        }
        // It's our turn, so game_state will not change on the server.
        if (gameState.status.equals("not started") || color != turn) {
            scheduleUpdateGameState();
        }
        else {
            cancelTimer();
        }
    }

    public void onMakeMove(Point from, Point to) {
        // chess board panel has a set of possible moves, so we are guaranteed
        // to have a valid move here and only need to send it to server.
        JSONObject response = httpManager.makeMove(new Move(from, to), gameId);
        if (!checkResponseStatus(response)) {
            return;
        }
        JSONObject result = (JSONObject) response.get("result");
        GameState gameState = GameState.fromJSON((JSONObject) result.get("game_state"));
        Color color = Utils.fromString((String) result.get("color"));
        Color turn = Utils.fromString((String) result.get("turn"));
        if (handleGameEnding(gameState)) {
            boardPanel.updateBoard(
                    new GameState(gameState.pieces, new ArrayList<>(), gameState.status), color, turn);
            return;
        }
        boardPanel.updateBoard(gameState, color, turn);
        scheduleUpdateGameState();
    }
}
