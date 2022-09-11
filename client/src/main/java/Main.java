import javax.imageio.ImageIO;
import javax.swing.*;
import javax.swing.border.EmptyBorder;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

public class Main {
    private final JPanel gui = new JPanel(new BorderLayout(3, 3));

    Main() {
        initializeGui();
    }

    public static void main(String[] args) {
        Runnable r = () -> {
            Main cg = new Main();

            JFrame f = new JFrame("ChessGameBuilder");
            f.add(cg.getGui());
            // Ensures JVM closes after frame(s) closed and
            // all non-daemon threads are finished
            f.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
            // See https://stackoverflow.com/a/7143398/418556 for demo.
            f.setLocationByPlatform(true);

            // ensures the frame is the minimum size it needs to be
            // in order display the components within it
            f.pack();
            // ensures the minimum size is enforced.
            f.setMinimumSize(new Dimension(f.getWidth(), f.getHeight() + 7));
            f.setVisible(true);
        };
        // Swing GUIs should be created and updated on the EDT
        // http://docs.oracle.com/javase/tutorial/uiswing/concurrency
        SwingUtilities.invokeLater(r);
    }

    public static Map<String, Image> getPieceImages() {
        BufferedImage all;
        try {
            all = ImageIO.read(new File("resources/chess.png"));
        } catch (IOException ex) {
            System.out.println("Can't read chess pieces image file.");
            return new HashMap<>();
        }
        HashMap<String, Image> pieceImages = new HashMap<>();
        final String[] pieceNames = { "king", "queen", "bishop", "knight",
                                      "rook", "pawn" };
        final String[] pieceColors = { "white", "black" };
        for (int y = 0; y < 2; ++y) {
            for (int x = 0; x < 6; ++x) {
                pieceImages.put(pieceNames[x] + pieceColors[y],
                                all.getSubimage(200 * x, 200 * y, 200, 200));
            }
        }
        return pieceImages;
    }

    public final void initializeGui() {
        gui.setBorder(new EmptyBorder(5, 5, 5, 5));
        // TODO: replace with a separate layout of buttons.
        JToolBar tools = new JToolBar();
        tools.setFloatable(false);
        gui.add(tools, BorderLayout.PAGE_START);
        Action newGameAction = new AbstractAction("New game") {
            @Override public void actionPerformed(ActionEvent e) {
                return;
            }
        };
        tools.add(newGameAction);

        ArrayList<Piece> pieces = new ArrayList<>();
        pieces.add(new Piece("rook", Color.BLACK, 0, 0));
        pieces.add(new Piece("king", Color.WHITE, 7, 7));

        JPanel chessBoard = new ChessBoardPanel(pieces, getPieceImages());
        chessBoard.setBorder(new EmptyBorder(8, 8, 8, 8));
        Color background = new Color(255, 255, 255);
        chessBoard.setBackground(background);

        JPanel boardConstrain = new JPanel(new GridBagLayout());
        boardConstrain.setBackground(background);
        boardConstrain.add(chessBoard);
        gui.add(boardConstrain);
    }

    public final JComponent getGui() {
        return gui;
    }
}