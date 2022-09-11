import javax.swing.*;
import java.awt.*;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.awt.event.MouseMotionListener;
import java.util.ArrayList;
import java.util.Map;

public class ChessBoardPanel extends JPanel {
    private final Map<String, Image> images;
    private ArrayList<Piece> pieces;
    private Piece selectedPiece = null;
    private Point selectedPiecePosition = null;

    public ChessBoardPanel(ArrayList<Piece> pieces, Map<String, Image> images) {
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
            if (p == selectedPiece) {
                continue;
            }
            g.drawImage(images.get(p.imageName).getScaledInstance(width, height,
                                                                  Image.SCALE_SMOOTH),
                        p.getX() * width, p.getY() * height, this);
        }
        // Paint selected piece last to make it appear on top of other pieces.
        if (selectedPiece != null) {
            g.drawImage(images.get(selectedPiece.imageName)
                              .getScaledInstance(width, height,
                                                 Image.SCALE_SMOOTH),
                        selectedPiecePosition.x - width / 2,
                        selectedPiecePosition.y - height / 2, this);
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

    private Point getCellByPosition(int x, int y) {
        return new Point(x / (getSize().width / 8), y / (getSize().height / 8));
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
                Point releaseCell = getCellByPosition(e.getX(), e.getY());
                if (releaseCell.x >= 0 && releaseCell.x < 8
                        || releaseCell.y >= 0 && releaseCell.y < 8) {
                    int pieceIndex = pieces.indexOf(
                            new Piece("", null, releaseCell.x, releaseCell.y));
                    if (pieceIndex != -1) {
                        if (pieces.get(pieceIndex) != selectedPiece) {
                            pieces.remove(pieceIndex);
                        }
                    }
                    selectedPiece.move(releaseCell.x, releaseCell.y);
                }
                selectedPiece = null;
                selectedPiecePosition = null;
                thisPanel.repaint();
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
