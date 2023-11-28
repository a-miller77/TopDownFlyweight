package project;

import javafx.fxml.FXML;
import javafx.scene.control.Label;
import javafx.scene.layout.Pane;

/**
 * This class is both the controller for the main FXML window
 * and represents nothing but the GUI, ideally.
 *
 * Ideally, it will hold some domain class that does most of the work.
 */
public class Controller {
    @FXML
    private Label message; // white text
    @FXML
    private Pane thePane; // The big open MSOE-red space you can do whatever you want with

    @FXML
    public void initialize() {
        message.setText("The message text can be set from the controller.");
    }
}
