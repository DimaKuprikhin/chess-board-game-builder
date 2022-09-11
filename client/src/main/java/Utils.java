import javax.imageio.ImageIO;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

public class Utils {
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
}
