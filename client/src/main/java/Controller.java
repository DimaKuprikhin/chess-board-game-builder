import java.awt.*;
import java.io.File;
import java.net.http.HttpClient;
import java.util.List;

public class Controller {
    private ChessBoardPanel boardPanel;

    public void addBoard(ChessBoardPanel boardPanel) {
        this.boardPanel = boardPanel;
    }

    public void createGame(File scriptPath, String playAs) {
        // called by `CreateGameWindow` when create button clicked. It takes
        // values from filled form fields and send request to server.
        
    }

    public void onCreateGameButton() {
        // show a form with field that user should fill. Disable tool buttons.
        new CreateGameWindow(this);
    }

    public void onJoinGameButton() {
        // send request to join a game to server. If success,
        // `onMoveFromServer` will be called with appropriate game state.
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
