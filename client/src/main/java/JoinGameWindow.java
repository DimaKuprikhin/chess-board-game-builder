import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;

public class JoinGameWindow {
    private final Controller controller;

    JoinGameWindow(Controller controller) {
        this.controller = controller;
        setupGUI(new JFrame("Присоединение к игре"));
    }

    private void setupGUI(JFrame frame) {
        frame.setSize(320, 220);
        frame.setResizable(false);
        frame.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Container pane = frame.getContentPane();
        pane.setLayout(null);

        JLabel linkLabel = new JLabel("Код для присоединения:");
        linkLabel.setFont(new Font("Arial", Font.PLAIN, 18));
        linkLabel.setSize(260, 20);
        linkLabel.setLocation(30, 30);
        pane.add(linkLabel);

        JTextField link = new JTextField();
        link.setFont(new Font("Arial", Font.PLAIN, 24));
        link.setSize(260, 30);
        link.setLocation(30, 60);
        pane.add(link);

        JButton linkGameButton = new JButton("Присоединиться");
        linkGameButton.setFont(new Font("Arial", Font.PLAIN, 24));
        linkGameButton.setSize(260, 40);
        linkGameButton.setLocation(30, 100);
        linkGameButton.addActionListener(new AbstractAction() {
            @Override public void actionPerformed(ActionEvent e) {
                frame.dispose();
                controller.joinGame(link.getText());
            }
        });
        pane.add(linkGameButton);

        frame.setVisible(true);
    }
}
