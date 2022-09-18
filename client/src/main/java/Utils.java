import javax.imageio.ImageIO;
import javax.swing.*;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.*;
import java.nio.file.Files;
import java.util.HashMap;
import java.util.Map;
import java.util.Random;

public class Utils {
    private static final Random rnd = new Random();

    public static Map<String, Image> getPieceImages() {
        BufferedImage all = null;
        try (InputStream stream = Utils.class.getResourceAsStream("chess.png")) {
            assert stream != null;
            all = ImageIO.read(stream);
        } catch (Exception ex) {
            Utils.showError("Ошибка", "Не удалось прочитать файл изображений.");
            System.exit(1);
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

    public static String readFile(File file) throws IOException {
        return Files.readString(file.toPath());
    }

    public static void showError(String title, String message) {
        JOptionPane.showMessageDialog(null, message, title, JOptionPane.ERROR_MESSAGE);
    }

    public static void showInfo(String title, String message) {
        JOptionPane.showMessageDialog(null, message, title, JOptionPane.INFORMATION_MESSAGE);
    }

    public static int randomInt(int bound) {
        return rnd.nextInt(bound);
    }

    public static Color fromString(String color) {
        if (color.equals("white")) {
            return Color.WHITE;
        }
        if (color.equals("black")) {
            return Color.BLACK;
        }
        return null;
    }
}
