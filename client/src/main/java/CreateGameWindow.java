import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.io.File;

public class CreateGameWindow {
    private final Controller controller;
    private File selectedFile = null;

    public CreateGameWindow(Controller controller) {
        this.controller = controller;
        this.setupGUI(new JFrame("Настройки игры"));
    }

    private void setupGUI(JFrame frame) {
        frame.setSize(350, 260);
        frame.setResizable(false);
        frame.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        Container pane = frame.getContentPane();
        pane.setLayout(null);

        JLabel scriptLabel = new JLabel("Скрипт");
        scriptLabel.setFont(new Font("Arial", Font.PLAIN, 20));
        scriptLabel.setSize(100, 20);
        scriptLabel.setLocation(20, 20);
        pane.add(scriptLabel);

        JButton chooseScriptButton = new JButton("Выбрать файл");
        chooseScriptButton.setFont(new Font("Arial", Font.PLAIN, 16));
        chooseScriptButton.setSize(180, 30);
        chooseScriptButton.setLocation(150, 20);
        chooseScriptButton.addActionListener(new AbstractAction() {
            @Override public void actionPerformed(ActionEvent e) {
                JFileChooser chooser = new JFileChooser();
                chooser.setDialogTitle("Выбрать скрипт");
                chooser.setFileSelectionMode(JFileChooser.FILES_ONLY);
                if (chooser.showOpenDialog(null)
                        == JFileChooser.APPROVE_OPTION) {
                    selectedFile = chooser.getSelectedFile();
                    chooseScriptButton.setText(selectedFile.getName());
                }
            }
        });
        pane.add(chooseScriptButton);

        JLabel colorLabel = new JLabel("Играть как");
        colorLabel.setFont(new Font("Arial", Font.PLAIN, 20));
        colorLabel.setSize(130, 20);
        colorLabel.setLocation(20, 60);
        pane.add(colorLabel);

        final Font radioButtonFont = new Font("Arial", Font.PLAIN, 17);
        JRadioButton asWhiteRButton = new JRadioButton("Белые");
        asWhiteRButton.setHorizontalTextPosition(JRadioButton.CENTER);
        asWhiteRButton.setHorizontalAlignment(JRadioButton.CENTER);
        asWhiteRButton.setVerticalTextPosition(JRadioButton.BOTTOM);
        asWhiteRButton.setFont(radioButtonFont);
        asWhiteRButton.setSelected(false);
        asWhiteRButton.setSize(100, 40);
        asWhiteRButton.setLocation(20, 100);
        pane.add(asWhiteRButton);

        JRadioButton asRandomRButton = new JRadioButton("Случайно");
        asRandomRButton.setHorizontalTextPosition(JRadioButton.CENTER);
        asWhiteRButton.setHorizontalAlignment(JRadioButton.CENTER);
        asRandomRButton.setVerticalTextPosition(JRadioButton.BOTTOM);
        asRandomRButton.setFont(radioButtonFont);
        asRandomRButton.setSelected(true);
        asRandomRButton.setSize(100, 40);
        asRandomRButton.setLocation(130, 100);
        pane.add(asRandomRButton);

        JRadioButton asBlackRButton = new JRadioButton("Черные");
        asBlackRButton.setHorizontalTextPosition(JRadioButton.CENTER);
        asWhiteRButton.setHorizontalAlignment(JRadioButton.CENTER);
        asBlackRButton.setVerticalTextPosition(JRadioButton.BOTTOM);
        asBlackRButton.setFont(radioButtonFont);
        asBlackRButton.setSelected(false);
        asBlackRButton.setSize(100, 40);
        asBlackRButton.setLocation(240, 100);
        pane.add(asBlackRButton);

        ButtonGroup radioButtonsGroup = new ButtonGroup();
        radioButtonsGroup.add(asWhiteRButton);
        radioButtonsGroup.add(asRandomRButton);
        radioButtonsGroup.add(asBlackRButton);

        JButton createButton = new JButton("Создать");
        createButton.setFont(new Font("Arial", Font.PLAIN, 24));
        createButton.setSize(160, 40);
        createButton.setLocation(80, 160);
        createButton.addActionListener(new AbstractAction() {
            @Override public void actionPerformed(ActionEvent e) {
                if (selectedFile == null) {
                    String message
                            = "Для создания игры, необходимо выбрать файл скрипта";
                    String title = "Ошибка при создании игры";
                    JOptionPane.showMessageDialog(null, message, title,
                                                  JOptionPane.ERROR_MESSAGE);
                }
                String playAs;
                if (asWhiteRButton.isSelected()) {
                    playAs = "white";
                } else if (asRandomRButton.isSelected()) {
                    playAs = "random";
                } else {
                    playAs = "black";
                }
                controller.createGame(selectedFile, playAs);
            }
        });
        pane.add(createButton);

        frame.setVisible(true);
    }
}
