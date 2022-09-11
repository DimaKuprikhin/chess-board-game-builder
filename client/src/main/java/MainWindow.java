import javax.swing.*;
import javax.swing.border.EmptyBorder;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.util.ArrayList;

public class MainWindow {
    private final JPanel mainPanel = new JPanel(new BorderLayout(3, 3));
    private final Controller controller = new Controller();

    MainWindow() {
        setupGUI(new JFrame("ChessBoardGameBuilder"));
    }

    public static void main(String[] args) {
        Runnable r = () -> {
            MainWindow cg = new MainWindow();
        };
        // Swing GUIs should be created and updated on the EDT
        // http://docs.oracle.com/javase/tutorial/uiswing/concurrency
        SwingUtilities.invokeLater(r);
    }

    public final void setupGUI(JFrame mainFrame) {
        mainPanel.setBorder(new EmptyBorder(5, 5, 5, 5));
        // TODO: replace with a separate layout of buttons.
        JToolBar tools = new JToolBar();
        tools.setOrientation(JToolBar.VERTICAL);
        tools.setFloatable(false);
        tools.setLayout(new GridLayout(16, 1, 0, 0));
        mainPanel.add(tools, BorderLayout.LINE_START);
        tools.add(new AbstractAction("Создать игру") {
            @Override public void actionPerformed(ActionEvent e) {
                controller.onCreateGameButton();
            }
        });
        tools.add(new AbstractAction("Присоединиться к игре") {
            @Override public void actionPerformed(ActionEvent e) {
                controller.onJoinGameButton();
            }
        });

        ArrayList<Piece> pieces = new ArrayList<>();
        pieces.add(new Piece("rook", Color.BLACK, 0, 0));
        pieces.add(new Piece("king", Color.WHITE, 7, 7));

        ChessBoardPanel chessBoard = new ChessBoardPanel(pieces,
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
        mainFrame.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
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