import javax.swing.*;
import javax.swing.border.EmptyBorder;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.util.ArrayList;

public class MainWindow {
    private final JPanel mainPanel = new JPanel(new BorderLayout(3, 3));
    private final Controller controller;
    private AbstractAction createGame = null;
    private AbstractAction joinGame = null;
    private AbstractAction resign = null;

    MainWindow(Controller controller) {
        this.controller = controller;
        setupGUI(new JFrame("ChessBoardGameBuilder"));
    }

    public static void main(String[] args) {
        Runnable r = () -> {
            boolean useLocalServer = args.length > 0 && args[0].equals(
                    "--use-local-server");
            MainWindow cg = new MainWindow(new Controller(useLocalServer));
        };
        // Swing GUIs should be created and updated on the EDT
        // http://docs.oracle.com/javase/tutorial/uiswing/concurrency
        SwingUtilities.invokeLater(r);
    }

    public void disableButtons(String status) {
        if (status.equals("running")) {
            createGame.setEnabled(false);
            joinGame.setEnabled(false);
            resign.setEnabled(true);
        }
        else {
            createGame.setEnabled(true);
            joinGame.setEnabled(true);
            resign.setEnabled(false);
        }
    }

    public void setupGUI(JFrame mainFrame) {
        mainPanel.setBorder(new EmptyBorder(5, 5, 5, 5));
        // TODO: replace with a separate layout of buttons.
        JToolBar tools = new JToolBar();
        tools.setOrientation(JToolBar.VERTICAL);
        tools.setFloatable(false);
        tools.setLayout(new GridLayout(16, 1, 0, 0));
        mainPanel.add(tools, BorderLayout.LINE_START);
        this.createGame = new AbstractAction("Создать игру") {
            @Override public void actionPerformed(ActionEvent e) {
                controller.onCreateGameButton();
            }
        };
        this.joinGame = new AbstractAction("Присоединиться к игре") {
            @Override public void actionPerformed(ActionEvent e) {
                controller.onJoinGameButton();
            }
        };
        this.resign = new AbstractAction("Сдаться") {
            @Override public void actionPerformed(ActionEvent e) {
                controller.onResign();
            }
        };
        tools.add(this.createGame);
        tools.add(this.joinGame);
        tools.add(this.resign);
        this.resign.setEnabled(false);
        controller.addMainWindow(this);

        ArrayList<Piece> pieces = new ArrayList<>();

        ChessBoardPanel chessBoard = new ChessBoardPanel(controller, pieces,
                                                         Utils.getPieceImages());
        chessBoard.setBorder(new EmptyBorder(8, 8, 8, 8));
        Color background = new Color(255, 255, 255);
        chessBoard.setBackground(background);
        controller.addBoard(chessBoard);

        JPanel boardConstrain = new JPanel(new GridBagLayout());
        boardConstrain.setBackground(background);
        boardConstrain.add(chessBoard);
        mainPanel.add(boardConstrain);

        mainFrame.add(mainPanel);
        // Ensures JVM closes after frame(s) closed and
        // all non-daemon threads are finished
        mainFrame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        // See https://stackoverflow.com/a/7143398/418556 for demo.
        mainFrame.setLocationByPlatform(true);
        // ensures the frame is the minimum size it needs to be
        // in order display the components within it
        mainFrame.pack();
        // ensures the minimum size is enforced.
        mainFrame.setMinimumSize(
                new Dimension(mainFrame.getWidth(), mainFrame.getHeight() + 7));
        mainFrame.setVisible(true);
    }
}