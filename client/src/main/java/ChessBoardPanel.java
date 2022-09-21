import javax.swing.*;
import java.awt.*;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.awt.event.MouseMotionListener;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

public class ChessBoardPanel extends JPanel {
    // Cache for scaled images of figures.
    private class ImageCache {
        // Size of cached images.
        public int cachedImagesSize = 0;
        public Map<String, Image> cache = new HashMap<>();
    }

    private final Controller controller;
    private final Map<String, Image> images;
    private ArrayList<Piece> pieces;
    private ArrayList<Move> possibleMoves = new ArrayList<>();
    private Color playerColor = null;
    private Color turn = null;
    private Piece selectedPiece = null;
    private Point selectedPiecePosition = null;
    private final ImageCache imageCache = new ImageCache();

    public ChessBoardPanel(Controller controller, ArrayList<Piece> pieces, Map<String, Image> images) {
        this.controller = controller;
        this.pieces = pieces;
        this.images = images;
        this.addMouseListeners();
    }

    @Override public void paint(Graphics g) {
        Dimension dimension = this.getSize();
        int width = dimension.width / 8;
        int height = dimension.height / 8;
        for (int y = 0; y < 8; y++) {
            for (int x = 0; x < 8; x++) {
                if ((x + y) % 2 == 0) {
                    g.setColor(new Color(235, 235, 208));
                } else {
                    g.setColor(new Color(119, 148, 85));
                }
                g.fillRect(x * width, y * height, width, height);
            }
        }
        for (Piece p : pieces) {
            if (p.equals(selectedPiece)) {
                continue;
            }
            int x = p.getX() * width;
            int y = p.getY() * height;
            // Reverse board so our pieces always at the bottom.
            if (playerColor.equals(Color.WHITE)) {
                y = dimension.height - y - height;
            }
            // Use image from cache if we can.
            Image image;
            if (imageCache.cachedImagesSize == width) {
                // Try to get cached image.
                image = imageCache.cache.get(p.imageName);
                // Cache contains images of the right size, but doesn't have image
                // for figure that we need.
                if (image == null) {
                    image = images.get(p.imageName).getScaledInstance(width, height, Image.SCALE_SMOOTH);
                    imageCache.cache.put(p.imageName, image);
                }
            }
            else {
                // Clear cache and set new cached images size (probably, window was
                // resized).
                image = images.get(p.imageName).getScaledInstance(width, height, Image.SCALE_SMOOTH);
                imageCache.cache = new HashMap<>();
                imageCache.cache.put(p.imageName, image);
                imageCache.cachedImagesSize = width;
            }
            g.drawImage(image, x, y, this);
        }
        if (selectedPiece != null && selectedPiece.color == playerColor) {
            for (Object moveObj : possibleMoves.stream()
                                               .filter(m -> m.from.x == selectedPiece.getX()
                                                       && m.from.y == selectedPiece.getY())
                                               .toArray()) {
                Move move = (Move) moveObj;
                g.setColor(new Color(0, 0, 255, 64));
                int radius = width / 8;
                int y = move.to.y * height + height / 2;
                if (playerColor == Color.WHITE) {
                    y = dimension.height - y;
                }
                y -= radius;
                g.fillOval(move.to.x * width + width / 2 - radius,
                           y, 2 * radius, 2 * radius);
            }
        }
        // Paint selected piece last to make it appear on top of other pieces.
        if (selectedPiece != null) {
            int x = selectedPiecePosition.x - width / 2;
            int y = selectedPiecePosition.y - height / 2;
            g.drawImage(images.get(selectedPiece.imageName)
                              .getScaledInstance(width, height,
                                                 Image.SCALE_SMOOTH),
                        x, y, this);
        }
    }

    @Override public Dimension getPreferredSize() {
        Dimension d = super.getPreferredSize();
        Dimension prefSize;
        Component c = getParent();
        if (c == null) {
            prefSize = new Dimension((int) d.getWidth(), (int) d.getHeight());
        } else if (c.getWidth() > d.getWidth()
                && c.getHeight() > d.getHeight()) {
            prefSize = c.getSize();
        } else {
            prefSize = d;
        }
        int w = (int) prefSize.getWidth();
        int h = (int) prefSize.getHeight();
        int s = Math.max(256, Math.min(w, h) / 8 * 8);
        return new Dimension(s, s);
    }

    public void updateBoard(GameState gameState, Color playerColor, Color turn) {
        this.pieces = gameState.pieces;
        this.possibleMoves = gameState.possibleMoves;
        this.playerColor = playerColor;
        this.turn = turn;
        this.repaint();
    }

    private Point getCellByPosition(int x, int y) {
        if (playerColor.equals(Color.BLACK)) {
            return new Point(x / (getSize().width / 8), y / (getSize().height / 8));
        }
        return new Point(x / (getSize().width / 8), (getSize().height - y) / (getSize().height / 8));
    }

    private void addMouseListeners() {
        ChessBoardPanel thisPanel = this;
        this.addMouseMotionListener(new MouseMotionListener() {
            @Override public void mouseDragged(MouseEvent e) {
                if (selectedPiece == null) {
                    return;
                }
                selectedPiecePosition = new Point(e.getX(), e.getY());
                thisPanel.repaint();
            }

            @Override public void mouseMoved(MouseEvent e) {

            }
        });
        this.addMouseListener(new MouseListener() {
            @Override public void mouseClicked(MouseEvent e) {

            }

            @Override public void mousePressed(MouseEvent e) {
                if (selectedPiece != null) {
                    return;
                }
                Point pressedCell = getCellByPosition(e.getX(), e.getY());
                int pieceIndex = pieces.indexOf(
                        new Piece("", null, pressedCell.x, pressedCell.y));
                selectedPiece = (pieceIndex == -1 ? null :
                                 pieces.get(pieceIndex));
                if (selectedPiece != null) {
                    selectedPiecePosition = new Point(e.getX(), e.getY());
                    thisPanel.repaint();
                }
            }

            @Override public void mouseReleased(MouseEvent e) {
                if (selectedPiece == null) {
                    return;
                }
                if (playerColor != turn || selectedPiece.color != turn) {
                    selectedPiece = null;
                    selectedPiecePosition = null;
                    thisPanel.repaint();
                    return;
                }
                Point from = null;
                Point releaseCell = getCellByPosition(e.getX(), e.getY());
                Move move = new Move(new Point(selectedPiece.getX(), selectedPiece.getY()),
                                     releaseCell);
                if (possibleMoves.contains(move)
                        && releaseCell.x >= 0 && releaseCell.x < 8
                        && releaseCell.y >= 0 && releaseCell.y < 8) {
                    int pieceIndex = pieces.indexOf(
                            new Piece("", null, releaseCell.x, releaseCell.y));
                    if (pieceIndex != -1) {
                        if (pieces.get(pieceIndex) != selectedPiece) {
                            pieces.remove(pieceIndex);
                        }
                    }
                    from = new Point(selectedPiece.getX(), selectedPiece.getY());
                    selectedPiece.move(releaseCell.x, releaseCell.y);
                }
                selectedPiece = null;
                selectedPiecePosition = null;
                thisPanel.repaint();
                if (from != null) {
                    controller.onMakeMove(from, releaseCell);
                }
            }

            @Override public void mouseEntered(MouseEvent e) {

            }

            @Override public void mouseExited(MouseEvent e) {
                selectedPiece = null;
                selectedPiecePosition = null;
                thisPanel.repaint();
            }
        });
    }
}
