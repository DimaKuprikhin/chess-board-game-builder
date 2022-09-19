import javax.swing.*;
import java.awt.*;

public class LinkWindow {
    private final String link;
    private final JFrame frame;

    LinkWindow(String link) {
        this.link = link;
        this.frame = new JFrame("Код для присоединения");
        setupGUI(this.frame);
    }

    private void setupGUI(JFrame frame) {
        frame.setResizable(false);
        frame.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Container pane = frame.getContentPane();
        pane.setLayout(null);

        JTextField link = new JTextField(this.link);
        link.setFont(new Font("Arial", Font.PLAIN, 30));
        link.setSize(link.getPreferredSize());
        link.setEditable(false);
        pane.add(link);
        frame.setSize(Math.max(280, link.getWidth() + 60), 140);
        link.setLocation((frame.getWidth() - link.getWidth()) / 2, 30);

        frame.setVisible(true);
    }

    public void dispose() {
        this.frame.dispose();
    }
}
