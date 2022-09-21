import org.json.simple.JSONObject;

import java.awt.*;
import java.util.ArrayList;
import java.util.Timer;
import java.util.TimerTask;

public class Controller {
    private ChessBoardPanel boardPanel;
    private final HttpManager httpManager;
    private Long gameId = null;
    private Timer timer = new Timer();
    private LinkWindow linkWindow = null;
    private MainWindow mainWindow = null;

    public Controller(boolean useLocalServer) {
        if (useLocalServer) {
            this.httpManager = new HttpManager("http", "localhost", 5000);
        }
        else {
            this.httpManager = new HttpManager("http", "51.250.76.192", 8080);
        }
    }

    public void addBoard(ChessBoardPanel boardPanel) {
        this.boardPanel = boardPanel;
    }

    public void addMainWindow(MainWindow mainWindow) {
        this.mainWindow = mainWindow;
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
        // If timer is null and gameId is set, it means this is the first time
        // `scheduleUpdateGameState()` was called for the game.
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

    private synchronized boolean handleGameEnding(GameState gameState) {
        // If gameId is null, that means that concurrent thread has already
        // handled an ended game, and we don't need to do anything.
        if (gameId == null) {
            return true;
        }

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
            // The game ended, and it's guaranteed that game state won't change
            // anymore.
            gameId = null;
            if (timer != null) {
                timer.cancel();
                timer = null;
            }
            // Enable 'create game` and `join game` buttons.
            mainWindow.disableButtons("not started");
            return true;
        }
        return false;
    }

    public void createGame(String script, String playAs) {
        // Send request to load the chosen script to server.
        JSONObject response = httpManager.loadScript(script);
        if (!checkResponseStatus(response)) {
            return;
        }

        // Send request to create game with returned `script_id`.
        JSONObject result = (JSONObject) response.get("result");
        response = httpManager.createGame((long) result.get("script_id"), playAs);
        if (checkResponseStatus(response)) {
            // If request was successful, save `game_id`, show window with the link
            // and start timer to update game state.
            result = (JSONObject) response.get("result");
            gameId = (Long) result.get("id");
            mainWindow.disableButtons("running");
            linkWindow = new LinkWindow((String) result.get("link"));
            scheduleUpdateGameState();
        }
    }

    public void onCreateGameButton() {
        // Show a form with field that user should fill.
        new CreateGameWindow(this);
    }

    public void joinGame(String link) {
        // Send request to join to a game by the link.
        JSONObject response = httpManager.joinGame(link);
        if (!checkResponseStatus(response)) {
            return;
        }

        // If request was successful, save `game_id`, update game state, and
        // start timer to update game state.
        JSONObject result = (JSONObject) response.get("result");
        GameState gameState = GameState.fromJSON((JSONObject) result.get("game_state"));
        Color color = Utils.fromString((String) result.get("color"));
        Color turn = Utils.fromString((String) result.get("turn"));
        this.gameId = (Long) result.get("game_id");
        boardPanel.updateBoard(gameState, color, turn);
        mainWindow.disableButtons("running");
        scheduleUpdateGameState();
    }

    public void onJoinGameButton() {
        // Show window with text field for join link.
        new JoinGameWindow(this);
    }

    private void updateGameState() {
        // Send request for actual game state.
        JSONObject response = httpManager.getGameState(gameId);
        if (!checkResponseStatus(response)) {
            return;
        }

        // Parse received JSON.
        JSONObject result = (JSONObject) response.get("result");
        GameState gameState = GameState.fromJSON((JSONObject) result.get("game_state"));
        Color color = Utils.fromString((String) result.get("color"));
        Color turn = Utils.fromString((String) result.get("turn"));

        // If game ended, handle it properly.
        if (handleGameEnding(gameState)) {
            boardPanel.updateBoard(
                    new GameState(gameState.pieces, new ArrayList<>(), gameState.status), color, turn);
            return;
        }

        // Update the board.
        boardPanel.updateBoard(gameState, color, turn);

        // If game is running and user has a window with join link, close this
        // window.
        if (!gameState.status.equals("not started") && linkWindow != null) {
            linkWindow.dispose();
            linkWindow = null;
        }

        // Reschedule `updateGameState()`.
        scheduleUpdateGameState();
    }

    public void onMakeMove(Point from, Point to) {
        // Chess board panel has a set of possible moves, so we are guaranteed
        // to have a valid move here and only need to send it to server.
        JSONObject response = httpManager.makeMove(new Move(from, to), gameId);
        if (!checkResponseStatus(response)) {
            return;
        }

        // Parse received JSON.
        JSONObject result = (JSONObject) response.get("result");
        GameState gameState = GameState.fromJSON((JSONObject) result.get("game_state"));
        Color color = Utils.fromString((String) result.get("color"));
        Color turn = Utils.fromString((String) result.get("turn"));

        // If game ended, handle it properly.
        if (handleGameEnding(gameState)) {
            boardPanel.updateBoard(
                    new GameState(gameState.pieces, new ArrayList<>(), gameState.status), color, turn);
            return;
        }

        // Update board.
        boardPanel.updateBoard(gameState, color, turn);
    }

    public void onResign() {
        // Send specific resign request.
        JSONObject response = httpManager.resign(gameId);
        if (!checkResponseStatus(response)) {
            return;
        }

        // Parse received JSON.
        JSONObject result = (JSONObject) response.get("result");
        GameState gameState = GameState.fromJSON((JSONObject) result.get("game_state"));
        Color color = Utils.fromString((String) result.get("color"));
        Color turn = Utils.fromString((String) result.get("turn"));

        // We must receive game state with "*_won" status.
        handleGameEnding(gameState);

        // Update board.
        boardPanel.updateBoard(
                new GameState(gameState.pieces, new ArrayList<>(), gameState.status), color, turn);
    }
}
