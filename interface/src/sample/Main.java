package sample;

import javafx.animation.*;
import javafx.application.Application;
import javafx.beans.property.*;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;
import javafx.scene.effect.InnerShadow;
import javafx.scene.layout.*;
import javafx.scene.paint.Color;
import javafx.scene.shape.Circle;
import javafx.scene.shape.Rectangle;
import javafx.scene.text.Text;
import javafx.stage.Stage;
import javafx.util.Duration;

import java.io.*;
import java.net.ConnectException;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;

// To start the Server: pip install flask
// python server.py

// Note to anyone who dares to read this (including myself):
// This monolithic chuck of code, although beautiful to some eyes, was coding at 3am under 2000mg of caffeine,
// although I was hearing the voice of my ancestors telling me comment and re-format my code, I took no heed to
// their calls, and as a result you are blessed with this masterpiece (I did comment it in the end).

public class Main extends Application {

    String dataSetNamePersistent = "Dataset Name";
    StringProperty dataSetName = new SimpleStringProperty();

    int barLength = 0;
    int imagesToTake = 1000;
    int totalImagesToTake = 0;
    int hours = 0;
    int numberOfSpecimens = 0;
    float minutes = 0;
    int sections = 0; // width of each step in the progress bar
    boolean objectDetectionType = false;
    boolean classificationType = false;
    boolean boundingBoxesType = false;
    boolean masksType = false;
    String serverURL = "http://localhost:5000/";

    // array of all the classes, each class looks like this: ['label', '# of specimens', '# of specimens imaged']
    String[][] classesArray = new String[20][];

    // total images taken by the robot
    IntegerProperty imagesTaken = new SimpleIntegerProperty();

    // current selected class by the user
    StringProperty currentClass = new SimpleStringProperty();

    // booleans listened to, to trigger / updates divers panes and nodes
    BooleanProperty updateList = new SimpleBooleanProperty();
    BooleanProperty collectData = new SimpleBooleanProperty();
    BooleanProperty updateCollectionInfo = new SimpleBooleanProperty();

    // track the object?
    BooleanProperty trackObject = new SimpleBooleanProperty();

    // lights settings: 1 = all lights on, 2 = alternate between lights, 3 = random lights on
    IntegerProperty lightsSettingsProp = new SimpleIntegerProperty();


    // bottom vertical limit
    IntegerProperty vLimit = new SimpleIntegerProperty();


    // horizontal limit
    IntegerProperty hLimit = new SimpleIntegerProperty();


    StringProperty robotName = new SimpleStringProperty(); // changes depending on the answer from the robot (ping)

    @Override
    public void start(Stage primaryStage) throws Exception{
        primaryStage.setTitle("ailu interface");

        // sidebar title
        Text robotID = new Text("AILU-0001 not ready");

        // sidebar buttons
        BorderPane configDataButton = largeSideBarButton("Configure Dataset");
        BorderPane robotControlsButton = largeSideBarButton("Robot Controls");
        BorderPane configRobotButton = largeSideBarButton("Configure Robot");
        Text datasetTitleSidebar = new Text(dataSetName.getValue());

        // sets default value
        vLimit.set(0);
        hLimit.set(360);

        // updates the name from the robot
        robotName.addListener(e->{
            robotID.setText(robotName.get());
        });

        // pings the robot at startup
        if(ping()){
            System.out.println("system ready");
            robotName.set("AILU-0001 ready");
        }else{
            System.out.println("system not ready");
            robotName.set("AILU-0001 not ready");
        }

        // create a persistent variable that is updated in real-time
        dataSetName.addListener(e->{

            if(dataSetName.getValue().equals("")){
                ;
            }else{
                dataSetNamePersistent = dataSetName.getValue();
                datasetTitleSidebar.setText(dataSetNamePersistent);
            }


        });

        // changes updateCollectionInfo when the current class changes (used to trigger other listeners)
        currentClass.addListener(e->{
            if(updateCollectionInfo.get()){
                updateCollectionInfo.set(false);
            }else{
                updateCollectionInfo.set(true);
            }

        });

        // changes updateCollectionInfo when the imagesTaken changes (used to trigger other listeners)
        imagesTaken.addListener(e->{
            if(imagesTaken.get() % imagesToTake == 0){
                if(updateCollectionInfo.get()){
                    updateCollectionInfo.set(false);
                }else{
                    updateCollectionInfo.set(true);
                }
            }

        });

        // CONFIG_DATA_HANDLER
        configDataButton.setOnMouseClicked(e->{

            collectData.set(false);

            // set the other buttons to normal colors
            configRobotButton.setBackground(new Background(new BackgroundFill(Color.rgb(45, 43, 43), CornerRadii.EMPTY, Insets.EMPTY)));
            configRobotButton.setRight(null);
            configRobotButton.setPadding(new Insets(12, 15, 12, 15));

            robotControlsButton.setBackground(new Background(new BackgroundFill(Color.rgb(45, 43, 43), CornerRadii.EMPTY, Insets.EMPTY)));
            robotControlsButton.setRight(null);
            robotControlsButton.setPadding(new Insets(12, 15, 12, 15));

            // set the colors right for the config button
            configDataButton.setBackground(new Background(new BackgroundFill(Color.rgb(32, 32, 32), CornerRadii.EMPTY, Insets.EMPTY)));
            configDataButton.setPadding(new Insets(0, 0, 0, 10));
            HBox widget = new HBox();
            widget.setMinWidth(10);
            widget.setMinHeight(40);
            widget.setBackground(new Background(new BackgroundFill(Color.rgb(89, 227, 149), CornerRadii.EMPTY, Insets.EMPTY)));
            configDataButton.setRight(widget);

        });


        //ROBOT CONTROLS HANDLER
        robotControlsButton.setOnMouseClicked(e->{

            collectData.set(false);

            // set the other buttons to normal colors
            configRobotButton.setBackground(new Background(new BackgroundFill(Color.rgb(45, 43, 43), CornerRadii.EMPTY, Insets.EMPTY)));
            configRobotButton.setRight(null);
            configRobotButton.setPadding(new Insets(12, 15, 12, 15));

            configDataButton.setBackground(new Background(new BackgroundFill(Color.rgb(45, 43, 43), CornerRadii.EMPTY, Insets.EMPTY)));
            configDataButton.setRight(null);
            configDataButton.setPadding(new Insets(12, 15, 12, 15));

            // set the colors right for the config button
            robotControlsButton.setBackground(new Background(new BackgroundFill(Color.rgb(32, 32, 32), CornerRadii.EMPTY, Insets.EMPTY)));
            robotControlsButton.setPadding(new Insets(0, 0, 0, 10));
            HBox widget = new HBox();
            widget.setMinWidth(10);
            widget.setMinHeight(40);
            widget.setBackground(new Background(new BackgroundFill(Color.rgb(89, 227, 149), CornerRadii.EMPTY, Insets.EMPTY)));
            robotControlsButton.setRight(widget);
        });


        //CONFIG ROBOT HANDLER
        configRobotButton.setOnMouseClicked(e->{

            collectData.set(false);

            // set the other buttons to normal colors
            configDataButton.setBackground(new Background(new BackgroundFill(Color.rgb(45, 43, 43), CornerRadii.EMPTY, Insets.EMPTY)));
            configDataButton.setRight(null);
            configDataButton.setPadding(new Insets(12, 15, 12, 15));

            robotControlsButton.setBackground(new Background(new BackgroundFill(Color.rgb(45, 43, 43), CornerRadii.EMPTY, Insets.EMPTY)));
            robotControlsButton.setRight(null);
            robotControlsButton.setPadding(new Insets(12, 15, 12, 15));


            // set the colors right for the config button
            configRobotButton.setBackground(new Background(new BackgroundFill(Color.rgb(32, 32, 32), CornerRadii.EMPTY, Insets.EMPTY)));
            configRobotButton.setPadding(new Insets(0, 0, 0, 10));
            HBox widget = new HBox();
            widget.setMinWidth(10);
            widget.setMinHeight(40);
            widget.setBackground(new Background(new BackgroundFill(Color.rgb(89, 227, 149), CornerRadii.EMPTY, Insets.EMPTY)));
            configRobotButton.setRight(widget);


        });

        // creates the title on top of the sidebar
        BorderPane topTitle = new BorderPane(robotID);
        topTitle.setBackground(new Background(new BackgroundFill(Color.rgb(89, 227, 149), CornerRadii.EMPTY, Insets.EMPTY)));

        BorderPane quickAccess = new BorderPane();
        BorderPane.setAlignment(datasetTitleSidebar,Pos.CENTER);
        datasetTitleSidebar.setFill(Color.rgb(219,205,205));
        quickAccess.setTop(datasetTitleSidebar);
        HBox bottomLine = new HBox();
        bottomLine.setMaxHeight(2);
        bottomLine.setMinHeight(2);
        bottomLine.setMaxWidth(180);
        bottomLine.setMinWidth(180);
        bottomLine.setBackground(new Background(new BackgroundFill(Color.rgb(219,205,205), CornerRadii.EMPTY, Insets.EMPTY)));
        BorderPane.setAlignment(bottomLine,Pos.CENTER);
        quickAccess.setCenter(bottomLine);

        VBox classListSidebar = new VBox();
        BorderPane.setAlignment(classListSidebar,Pos.CENTER);

        updateList.addListener(e->{

            if(updateList.get()){
                classListSidebar.getChildren().clear();
                for(String[] individualClass: classesArray) {

                    if (individualClass != null) {
                        classListSidebar.getChildren().addAll(classButton(individualClass[0]));
                    }

                }
                updateList.set(false);
            }

        });
        quickAccess.setBottom(classListSidebar);


        Pane menuSpacer = new Pane();
        menuSpacer.setMinHeight(100);

        // creates the side bar
        VBox sideBar = new VBox();
        sideBar.setBackground(new Background(new BackgroundFill(Color.rgb(45, 43, 43), CornerRadii.EMPTY, Insets.EMPTY)));
        sideBar.setMinWidth(200);
        BorderPane.setAlignment(sideBar,Pos.CENTER);
        BorderPane collectDataButtonInstance = collectDataButton();
        Region spacer1 = new Region();
        VBox.setVgrow(spacer1, Priority.ALWAYS);
        sideBar.getChildren().addAll(topTitle, configDataButton, robotControlsButton, configRobotButton,menuSpacer, quickAccess,spacer1, collectDataButtonInstance);



        // Create a BorderPane with a Text node in each of the five regions
        BorderPane root = new BorderPane();
        root.setRight(sideBar);
        root.setCenter(configDatasetPane());

        configDataButton.rightProperty().addListener(e ->{

            if(configDataButton.rightProperty() != null){
                root.setCenter(null);
                root.setCenter(configDatasetPane());

            }

        });

        configRobotButton.rightProperty().addListener(e ->{

            if(configRobotButton.rightProperty() != null){
                root.setCenter(null);
                root.setCenter(robotConfig());

            }

        });

        robotControlsButton.rightProperty().addListener(e ->{

            if(configRobotButton.rightProperty() != null){
                root.setCenter(null);
                root.setCenter(robotControls());

            }

        });



        collectData.addListener(e->{
            if(collectData.get()){
                root.setCenter(null);
                root.setCenter(collectDataGrid());
            }
            currentClass.set(classesArray[0][0]);
        });


        // Create the Scene
        Scene scene = new Scene(root, 1200, 720);
        primaryStage.setScene(scene);
        primaryStage.show();
    }

    // button to collect data in the sidebar
    public BorderPane collectDataButton(){

        BorderPane container = new BorderPane();
        container.setPadding(new Insets(12, 15, 12, 15));
        BorderPane button = new BorderPane();
        BorderPane.setAlignment(button,Pos.CENTER);
        Text buttonText = new Text("Gather Data");
        BorderPane.setAlignment(buttonText,Pos.CENTER);
        buttonText.setFill(Color.rgb(219,205,205));
        button.setMinWidth(180);
        button.setMinHeight(60);
        button.setBackground(new Background(new BackgroundFill(Color.rgb(45, 43, 43), CornerRadii.EMPTY, Insets.EMPTY)));
        button.setBorder(new Border(new BorderStroke(Color.rgb(89, 227, 149),BorderStrokeStyle.SOLID, CornerRadii.EMPTY, BorderWidths.DEFAULT)));

        button.setOnMouseEntered(e->{
            button.setBackground(new Background(new BackgroundFill(Color.rgb(32, 32, 32), CornerRadii.EMPTY, Insets.EMPTY)));
        });
        button.setOnMouseExited(e->{
            button.setBackground(new Background(new BackgroundFill(Color.rgb(45, 43, 43), CornerRadii.EMPTY, Insets.EMPTY)));
        });
        button.setOnMouseClicked(e->{
            collectData.set(true);
        });

        button.setCenter(buttonText);
        container.setCenter(button);

        return container;
    }

    // grid that shows when you press the collect data button
    public GridPane collectDataGrid(){

        GridPane grid = new GridPane();
        int intSections = 1000;
        if(numberOfSpecimens != 0){
            sections = (990 / numberOfSpecimens);
            intSections = (int)sections * numberOfSpecimens;
        }
        grid.setMinWidth(intSections);
        InnerShadow gridShadow = new InnerShadow(10, -5, 0, Color.BLACK);
        grid.setEffect(gridShadow);
        grid.setBackground(new Background(new BackgroundFill(Color.rgb(55, 55, 55), CornerRadii.EMPTY, Insets.EMPTY)));
        BorderPane.setAlignment(grid,Pos.CENTER_LEFT);

        grid.add(progressBar(), 1, 0);
        grid.add(progressInfo(), 1, 1);
        grid.add(progressControls(), 1, 2);

        return grid;
    }

    // buttons to images next specimen or re-take the images
    public HBox progressControls(){
        HBox container = new HBox();
        container.setAlignment(Pos.CENTER);
        container.setPadding(new Insets(50, 0, 0, 0));
        container.setSpacing(300);
        VBox reDo = new VBox();
        reDo.setAlignment(Pos.CENTER);
        reDo.setMinWidth(180);
        reDo.setMinHeight(60);
        Label reDoText = new Label("Re-take");
        reDoText.setTextFill(Color.rgb(219,205,205));
        reDoText.setAlignment(Pos.CENTER);
        reDo.getChildren().addAll(reDoText);
        reDo.setBorder(new Border(new BorderStroke(Color.rgb(89, 227, 149),BorderStrokeStyle.SOLID, CornerRadii.EMPTY, BorderWidths.DEFAULT)));

        VBox next = new VBox();
        next.setAlignment(Pos.CENTER);
        next.setMinWidth(180);
        next.setMinHeight(60);
        Label nextText = new Label("Image Next Specimen");
        nextText.setTextFill(Color.rgb(219,205,205));
        nextText.setAlignment(Pos.CENTER);
        next.getChildren().addAll(nextText);
        next.setBorder(new Border(new BorderStroke(Color.rgb(89, 227, 149),BorderStrokeStyle.SOLID, CornerRadii.EMPTY, BorderWidths.DEFAULT)));

        container.getChildren().addAll(reDo, next);
        container.setMinWidth(900);


        next.setOnMouseClicked(e->{

            // sends a post request to the server and waits
            run("normal");

            int index = 0;

            // timeline animation to increase images
            Timeline timeline = new Timeline();
            timeline.setCycleCount(imagesToTake);
            timeline.getKeyFrames().add(new KeyFrame(Duration.millis(30), b-> {
                    imagesTaken.set(imagesTaken.get() + 1);
                }));
            timeline.playFromStart();

            // finds the selected class and adds 1 to the number of specimens imaged
            for(String[] individualClass: classesArray) {
                if(individualClass != null){
                    if(individualClass[0].equals(currentClass.get())){
                        int specimenImaged = Integer.parseInt(individualClass[2]);
                        specimenImaged ++;
                        String[] newArray = new String[3];
                        newArray[0] = individualClass[0];
                        newArray[1] = individualClass[1];
                        newArray[2] = Integer.toString(specimenImaged);
                        classesArray[index] = newArray;
                    }
                    index ++;
                }

            }

        });

        reDo.setOnMouseClicked(e->{
            imagesTaken.set(imagesTaken.get() - imagesToTake);
            Timeline timeline = new Timeline();
            timeline.setCycleCount(imagesToTake);
            timeline.getKeyFrames().add(new KeyFrame(Duration.millis(3), b-> {
                // KeyFrame event handler
                imagesTaken.set(imagesTaken.get() + 1);
            }));
            timeline.playFromStart();

        });

        return container;
    }

    // sends a simple post request to the server
    // Note: although I haves experience with Restful APIs I never used java to send requests before,
    // a lot of this code will be similar to code you an find by seraching "Post / get requests java" on google
    // not copied and pasted though.
    public void setToSever(String command, int value){
        try{
            String setURL = serverURL + "set";
            URL url = new URL(setURL);
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setDoOutput(true);
            connection.setRequestMethod("POST");
            connection.setRequestProperty("Content-Type", "application/json");

            String request = "{\"command\":\""+command+"\",\"value\":\""+value+"\"}";
            OutputStream os = connection.getOutputStream();
            os.write(request.getBytes());
            os.flush();

            if (connection.getResponseCode() != HttpURLConnection.HTTP_CREATED) {
                throw new RuntimeException("Failed: HTTP error code: " + connection.getResponseCode());
            }
            BufferedReader br = new BufferedReader(new InputStreamReader((connection.getInputStream())));

            String responce;
            while ((responce = br.readLine()) != null) {
                System.out.println(responce);
            }
            connection.disconnect();

        } catch (MalformedURLException err) {

            err.printStackTrace();

        }catch (IOException err) {

            err.printStackTrace();

        }
    }

    public void run(String runType){
        try{
            String setURL = serverURL + "run";
            URL url = new URL(setURL);
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setDoOutput(true);
            connection.setRequestMethod("POST");
            connection.setRequestProperty("Content-Type", "application/json");


            String type;
            if(objectDetectionType){
                type = "object detection";
            }else {
                type = "classification";
            }

            String request = "{\"runType\":\""+runType+"\",\"dataSetName\":\""+dataSetNamePersistent+"\",\"label\":\""+currentClass.get()+"\"," +
                    "\"images\":\""+imagesToTake+"\",\"track\":\""+trackObject.get()+"\",\"lights\":\""+lightsSettingsProp.get()+"\"," +
                    "\"type\":\""+type+"\",\"bndBoxes\":\""+boundingBoxesType+"\",\"masks\":\""+masksType+"\", \"lowerLimit\":\""+vLimit.get()+"\"}";
            OutputStream os = connection.getOutputStream();
            os.write(request.getBytes());
            os.flush();

            if (connection.getResponseCode() != HttpURLConnection.HTTP_CREATED) {
                throw new RuntimeException("Failed: HTTP error code: " + connection.getResponseCode());
            }
            BufferedReader br = new BufferedReader(new InputStreamReader((connection.getInputStream())));

            String responce;
            while ((responce = br.readLine()) != null) {
                System.out.println(responce);
            }
            connection.disconnect();

        } catch (MalformedURLException err) {

            err.printStackTrace();

        }catch (IOException err) {

            err.printStackTrace();

        }
    }

    // diplays the percentages and other information below the progress bar
    public BorderPane progressInfo(){

        BorderPane container = new BorderPane();
        VBox localProgress = new VBox();
        localProgress.setAlignment(Pos.CENTER);
        localProgress.setMinWidth(480);
        localProgress.setPadding(new Insets(50, 0, 0, 0));
        Label currentClassText = new Label(currentClass.get());
        Label progressTextLocal = new Label("0%");
        Label progressTextImagesLocal = new Label("0 / 0");
        currentClassText.setTextFill(Color.rgb(219,205,205));
        currentClassText.setAlignment(Pos.CENTER);
        progressTextLocal.setTextFill(Color.rgb(219,205,205));
        progressTextLocal.setAlignment(Pos.CENTER);
        progressTextLocal.setStyle("-fx-font: 100 arial;");
        progressTextImagesLocal.setTextFill(Color.rgb(219,205,205));
        progressTextImagesLocal.setPadding(new Insets(5, 0, 0, 0));

        // for loops loop over the list of classes and look for the class we need
        for(String[] individualClass: classesArray) {
            if(individualClass != null){
                if(individualClass[0].equals(currentClass.get())){
                    float percentage = Float.parseFloat(individualClass[2]) / Float.parseFloat(individualClass[1]);
                    percentage = percentage *100;
                    String stringPercentage = String.format("%.1f", percentage);
                    progressTextLocal.setText(stringPercentage + "%");
                    progressTextImagesLocal.setText(Integer.toString(Integer.parseInt(individualClass[2]) * imagesToTake) + " / " + Integer.toString(Integer.parseInt(individualClass[1]) * imagesToTake));

                }
            }

        }
        currentClassText.setText(currentClass.get());

        // updates the info when updateCollectionInfo changes
        updateCollectionInfo.addListener(e->{
            for(String[] individualClass: classesArray) {
                if(individualClass != null){
                    if(individualClass[0].equals(currentClass.get())){
                        float percentage = Float.parseFloat(individualClass[2]) / Float.parseFloat(individualClass[1]);
                        percentage = percentage *100;
                        String stringPercentage = String.format("%.1f", percentage);
                        progressTextLocal.setText(stringPercentage + "%");
                        progressTextImagesLocal.setText(Integer.toString(Integer.parseInt(individualClass[2]) * imagesToTake) + " / " + Integer.toString(Integer.parseInt(individualClass[1]) * imagesToTake));

                    }
                }

            }
            currentClassText.setText(currentClass.get());

        });


        localProgress.getChildren().addAll(currentClassText, progressTextLocal, progressTextImagesLocal);
        container.setLeft(localProgress);

        // Global data collection progress
        VBox globalProgress = new VBox();
        globalProgress.setAlignment(Pos.CENTER);
        globalProgress.setMinWidth(480);
        globalProgress.setPadding(new Insets(50, 0, 0, 0));

        Label globalDatasetName = new Label(dataSetNamePersistent);
        float globalProgressFloat = (float)imagesTaken.get() / (float)totalImagesToTake;
        Label progressTextGlobal = new Label(Integer.toString((int)globalProgressFloat) + "%");
        Label progressTextImagesGlobal = new Label(Integer.toString(imagesTaken.get()) + " / " + Integer.toString(totalImagesToTake));
        globalDatasetName.setTextFill(Color.rgb(219,205,205));
        globalDatasetName.setAlignment(Pos.CENTER);
        progressTextGlobal.setTextFill(Color.rgb(219,205,205));
        progressTextGlobal.setAlignment(Pos.CENTER);
        progressTextGlobal.setStyle("-fx-font: 100 arial;");
        progressTextImagesGlobal.setTextFill(Color.rgb(219,205,205));
        progressTextImagesGlobal.setPadding(new Insets(5, 0, 0, 0));

        // updates when the number of classes changes
        imagesTaken.addListener(e->{
            for(String[] individualClass: classesArray) {
                if(individualClass != null){
                    if(individualClass[0].equals(currentClass.get())){
                        float globalProgressFloatlambda = (float)imagesTaken.get() / (float)totalImagesToTake;
                        globalProgressFloatlambda = globalProgressFloatlambda *100;
                        String stringGlobalProgress = String.format("%.1f", globalProgressFloatlambda);
                        progressTextGlobal.setText(stringGlobalProgress + "%");
                        progressTextImagesGlobal.setText(Integer.toString(imagesTaken.get()) + " / " + Integer.toString(totalImagesToTake));

                    }
                }

            }

        });

        // updates when the current selected class changes
        currentClass.addListener(e->{
            for(String[] individualClass: classesArray) {
                if(individualClass != null){
                    if(individualClass[0].equals(currentClass.get())){
                        float globalProgressFloatlambda = (float)imagesTaken.get() / (float)totalImagesToTake;
                        globalProgressFloatlambda = globalProgressFloatlambda *100;
                        String stringGlobalProgress = String.format("%.1f", globalProgressFloatlambda);
                        progressTextGlobal.setText(stringGlobalProgress + "%");
                        progressTextImagesGlobal.setText(Integer.toString(imagesTaken.get()) + " / " + Integer.toString(totalImagesToTake));

                    }
                }

            }

        });

        globalProgress.getChildren().addAll(globalDatasetName,progressTextGlobal, progressTextImagesGlobal);
        container.setRight(globalProgress);


        return container;
    }

    // Progress bar in top of the collect data pane
    public BorderPane progressBar(){
        int loopTotal = 0;
        barLength = 0;
        BorderPane container = new BorderPane();
        HBox bar = new HBox();
        bar.setMaxWidth(990);
        bar.setMinWidth(990);
        System.out.println(" the bar's max length is 990, and there are " + numberOfSpecimens + " specimens");
        bar.setMinHeight(150);
        HBox bottomLabel = new HBox();
        bottomLabel.setMaxWidth(990);
        bottomLabel.setMinWidth(990);
        if(numberOfSpecimens != 0){
            sections = (990 / numberOfSpecimens);
        }

        //create / updates the progress bar
        for(String[] individualClass: classesArray) {

            if (individualClass != null) {
                String name = individualClass[0];
                int amount = Integer.parseInt(individualClass[1]);
                int done = Integer.parseInt(individualClass[2]);
                Label classLabel = new Label(name);
                classLabel.setMinWidth(amount * sections);
                classLabel.setMaxWidth(amount * sections);
                int intSectionAmount = amount * sections;
                barLength = barLength + intSectionAmount;
                double doubleSections = amount * sections;
                System.out.println(amount + " * " + sections + " = " + intSectionAmount + " or " + doubleSections);
                classLabel.setTextFill(Color.rgb(219,205,205));
                classLabel.setAlignment(Pos.CENTER);

                for(int i = 0; i < done; i++){
                    loopTotal ++;
                    Pane block = new Pane();
                    block.setMaxWidth(sections);
                    block.setMinWidth(sections);
                    if(loopTotal == numberOfSpecimens){
                        System.out.println("last section");
                        block.setMaxWidth(sections + (990 - barLength));
                        block.setMinWidth(sections + (990 - barLength));
                    }
                    block.setMaxHeight(150);
                    block.setMinHeight(150);
                    block.setBackground(new Background(new BackgroundFill(Color.rgb(89, 227, 149, 1), CornerRadii.EMPTY, Insets.EMPTY)));
                    bar.getChildren().addAll(block);
                    FadeTransition popIn = new FadeTransition(Duration.millis(200), block);
                    popIn.setFromValue(0.1);
                    popIn.setToValue(1.0);
                    popIn.setCycleCount(1);
                    popIn.play(); // Start animation
                }

                for(int i = 0; i < (amount - done); i++){
                    loopTotal ++;
                    Pane block = new Pane();
                    block.setMaxWidth(sections);
                    block.setMinWidth(sections);
                    if(loopTotal == numberOfSpecimens){
                        System.out.println("last section");
                        block.setMaxWidth(sections + (990 - barLength));
                        block.setMinWidth(sections + (990 - barLength));
                    }

                    block.setMaxHeight(150);
                    block.setMinHeight(150);
                    if(currentClass.get() == null){
                        block.setBackground(new Background(new BackgroundFill(Color.rgb(89, 227, 149, 0.5), CornerRadii.EMPTY, Insets.EMPTY)));
                    }else{
                        if(currentClass.get().equals(name)){
                            block.setBackground(new Background(new BackgroundFill(Color.rgb(31, 155, 194, 0.8), CornerRadii.EMPTY, Insets.EMPTY)));
                        }else{
                            block.setBackground(new Background(new BackgroundFill(Color.rgb(89, 227, 149, 0.5), CornerRadii.EMPTY, Insets.EMPTY)));
                        }
                    }


                    bar.getChildren().addAll(block);
                    FadeTransition popIn = new FadeTransition(Duration.millis(800), block);
                    popIn.setFromValue(0.1);
                    popIn.setToValue(1.0);
                    popIn.setCycleCount(1);
                    popIn.play(); // Start animation
                }
                barLength ++;
                Pane block = new Pane();
                block.setMaxWidth(1);
                block.setMinWidth(1);
                block.setMaxHeight(150);
                block.setMinHeight(150);
                block.setBackground(new Background(new BackgroundFill(Color.rgb(219,205,205, 1), CornerRadii.EMPTY, Insets.EMPTY)));
                bar.getChildren().addAll(block);
                barLength ++;

                bottomLabel.getChildren().addAll(classLabel);

            }


        }
        System.out.println("loop total: " +loopTotal);
        container.setCenter(bar);
        container.setBottom(bottomLabel);

//         updates the progress bar when updateCollectionInfo changes
        updateCollectionInfo.addListener(e->{
            int loopTotalThing = 0;
            bar.getChildren().clear();
            bottomLabel.getChildren().clear();
            for(String[] individualClass: classesArray) {


                if (individualClass != null) {

                    String name = individualClass[0];
                    int amount = Integer.parseInt(individualClass[1]);
                    int done = Integer.parseInt(individualClass[2]);
                    Label classLabel = new Label(name);
                    classLabel.setMinWidth((amount) * sections);
                    classLabel.setMaxWidth((amount) * sections);
//                    bar.setMinWidth((amount) * sections);
//                    bar.setMaxWidth((amount) * sections);
                    int intSectionAmount = amount * (int)sections;
                    double doubleSections = amount * sections;
                    System.out.println(amount + " * " + sections + " = " + intSectionAmount + " or " + doubleSections);
                    classLabel.setTextFill(Color.rgb(219,205,205));
                    classLabel.setAlignment(Pos.CENTER);

                    for(int i = 0; i < done; i++){
                        loopTotalThing ++;
                        Pane block = new Pane();
                        block.setMaxWidth(sections);
                        block.setMinWidth(sections);
                        if(loopTotalThing == numberOfSpecimens){
                            System.out.println("last section");
                            block.setMaxWidth(sections + (990 - barLength));
                            block.setMinWidth(sections + (990 - barLength));
                        }
                        block.setMaxHeight(150);
                        block.setMinHeight(150);
                        block.setBackground(new Background(new BackgroundFill(Color.rgb(89, 227, 149, 1), CornerRadii.EMPTY, Insets.EMPTY)));
                        bar.getChildren().addAll(block);
                        FadeTransition popIn = new FadeTransition(Duration.millis(200), block);
                        popIn.setFromValue(0.1);
                        popIn.setToValue(1.0);
                        popIn.setCycleCount(1);
                        popIn.play();
                    }

                    for(int i = 0; i < (amount - done); i++){
                        loopTotalThing ++;
                        Pane block = new Pane();
                        block.setMaxWidth(sections);
                        block.setMinWidth(sections);
                        if(loopTotalThing == numberOfSpecimens){
                            System.out.println("last section");
                            block.setMaxWidth(sections + (990 - barLength));
                            block.setMinWidth(sections + (990 - barLength));
                        }
                        block.setMaxHeight(150);
                        block.setMinHeight(150);
                        if(currentClass.get() == null){
                            block.setBackground(new Background(new BackgroundFill(Color.rgb(89, 227, 149, 0.5), CornerRadii.EMPTY, Insets.EMPTY)));
                        }else{
                            if(currentClass.get().equals(name)){
                                block.setBackground(new Background(new BackgroundFill(Color.rgb(31, 155, 194, 0.8), CornerRadii.EMPTY, Insets.EMPTY)));
                            }else{
                                block.setBackground(new Background(new BackgroundFill(Color.rgb(89, 227, 149, 0.5), CornerRadii.EMPTY, Insets.EMPTY)));
                            }
                        }

                        bar.getChildren().addAll(block);
                        // simple fade animation
                        FadeTransition popIn = new FadeTransition(Duration.millis(100), block);
                        popIn.setFromValue(0.1);
                        popIn.setToValue(1.0);
                        popIn.setCycleCount(1);
                        popIn.play();
                    }
                    Pane block = new Pane();
                    block.setMaxWidth(2);
                    block.setMinWidth(2);
                    block.setMaxHeight(150);
                    block.setMinHeight(150);
                    block.setBackground(new Background(new BackgroundFill(Color.rgb(219,205,205, 1), CornerRadii.EMPTY, Insets.EMPTY)));
                    bar.getChildren().addAll(block);

                    bottomLabel.getChildren().addAll(classLabel);

                }


            }

            System.out.println("loop total in lambda: " +loopTotalThing);
            container.setCenter(bar);
            container.setBottom(bottomLabel);

        });

        return container;
    }

    // the three buttons on top of the sidebar
    public BorderPane largeSideBarButton(String text) {

        Text buttonText = new Text(text);
        buttonText.setFill(Color.rgb(219,205,205));
        BorderPane bPane = new BorderPane();
        bPane.setPadding(new Insets(12, 15, 12, 15));
        bPane.setCenter(buttonText);


        bPane.setOnMouseEntered(e->{
            bPane.setBackground(new Background(new BackgroundFill(Color.rgb(32, 32, 32), CornerRadii.EMPTY, Insets.EMPTY)));
        });

        bPane.setOnMouseExited(e->{
            if(bPane.getRight() == null) {
                bPane.setBackground(new Background(new BackgroundFill(Color.rgb(45, 43, 43), CornerRadii.EMPTY, Insets.EMPTY)));
            }
        });



        return bPane;
    }

    // these are the button to select a new class
    public BorderPane classButton(String text){

        BorderPane button = new BorderPane();
        Text label = new Text(text);
        label.setFill(Color.rgb(219,205,205));
        BorderPane.setAlignment(label,Pos.CENTER);
        button.setPadding(new Insets(5, 5, 5, 5));
        button.setCenter(label);

        button.setOnMouseClicked(e->{
            currentClass.set(label.getText());
        });

        currentClass.addListener(e->{
            if(currentClass.get().equals(label.getText())){
                button.setBackground(new Background(new BackgroundFill(Color.rgb(32, 32, 32), CornerRadii.EMPTY, Insets.EMPTY)));
            }else{
                button.setBackground(new Background(new BackgroundFill(Color.rgb(45, 43, 43), CornerRadii.EMPTY, Insets.EMPTY)));
            }
        });
        return button;
    }


    // create a grid pane as the main interactive pane to configure the dataset
    public GridPane configDatasetPane(){

        GridPane grid = new GridPane();
        grid.setMaxWidth(1000);
        InnerShadow gridShadow = new InnerShadow(10, -5, 0, Color.BLACK);
        grid.setEffect(gridShadow);
        grid.setBackground(new Background(new BackgroundFill(Color.rgb(55, 55, 55), CornerRadii.EMPTY, Insets.EMPTY)));
        BorderPane.setAlignment(grid,Pos.CENTER_LEFT);
        grid.setVgap(5);
        grid.setHgap(5);

        // enter the dataset name pane
        BorderPane datasetName = new BorderPane();
        datasetName.setPadding(new Insets(12, 15, 12, 15));
        Text datasetNameText = new Text("Dataset Name");
        datasetNameText.setFill(Color.rgb(219,205,205));
        BorderPane.setAlignment(datasetNameText,Pos.CENTER_LEFT);
        BorderPane dnDark = new BorderPane();
        dnDark.setMinSize(447, 56);
        dnDark.setBackground(new Background(new BackgroundFill(Color.rgb(45, 43, 43), CornerRadii.EMPTY, Insets.EMPTY)));
        dnDark.setPadding(new Insets(12, 15, 12, 15));
        TextField dnLabel = new TextField(dataSetNamePersistent);
        dataSetName.bind(dnLabel.textProperty());
        dnDark.setCenter(dnLabel);
        datasetName.setCenter(datasetNameText);
        datasetName.setBottom(dnDark);

        // classes pane
        BorderPane classes = new BorderPane();
        classes.setPadding(new Insets(12, 15, 12, 15));
        Text classesText = new Text("Classes");
        classesText.setFill(Color.rgb(219,205,205));
        BorderPane.setAlignment(classesText,Pos.CENTER_LEFT);
        VBox cDark = new VBox();
        cDark.setMinSize(447, 500);
        cDark.setBackground(new Background(new BackgroundFill(Color.rgb(45, 43, 43), CornerRadii.EMPTY, Insets.EMPTY)));
        cDark.setPadding(new Insets(12, 15, 12, 15));

        // pane at the bottom of the classes pane (add / remove class)
        HBox submitPane = new HBox();
        submitPane.setBackground(new Background(new BackgroundFill(Color.rgb(45, 43, 43), CornerRadii.EMPTY, Insets.EMPTY)));
        TextField className = new TextField();
        className.setMinWidth(150);
        TextField speciemenNumber = new TextField();
        speciemenNumber.setMaxWidth(50);
        BorderPane.setAlignment(speciemenNumber,Pos.CENTER);
        Button removeClass = new Button("Remove Last");
        Button addClass = new Button("Add New");
        HBox submitButtonPane = new HBox();
        submitButtonPane.setSpacing(12);
        submitButtonPane.getChildren().addAll(addClass, removeClass);
        submitPane.setSpacing(12);
        submitPane.getChildren().addAll(className, speciemenNumber, submitButtonPane);
        submitPane.setPadding(new Insets(12, 20, 12, 15));
        classes.setTop(classesText);
        classes.setCenter(cDark);
        classes.setBottom(submitPane);

        //this is the selection button on top of the pane to choose how many images of each object you need.
        BorderPane numberOfImages = new BorderPane();
        Text NOITitle = new Text("Number of images per object");
        NOITitle.setFill(Color.rgb(219,205,205));
        BorderPane.setAlignment(NOITitle,Pos.CENTER_LEFT);
        numberOfImages.setTop(NOITitle);
        numberOfImages.setMinWidth(400);
        numberOfImages.setMaxHeight(72);
        HBox selectNumber = new HBox();
        BorderPane oneThou = numberSelection("1000");
        BorderPane fiveThou = numberSelection("5000");
        BorderPane tenThou = numberSelection("10000");
        BorderPane fifteenThou = numberSelection("15000");

        selectNumber.getChildren().addAll(oneThou, fiveThou, tenThou, fifteenThou);
        numberOfImages.setCenter(selectNumber);


        VBox otherDataInfo = new VBox();
        otherDataInfo.setMinWidth(400);
        otherDataInfo.setMaxHeight(565);
        Text typeTitle = new Text("Dataset Type");
        typeTitle.setFill(Color.rgb(219,205,205));
        VBox dType = new VBox();

        // radio button to see if you want object detection
        HBox objectDetection = new HBox();
        objectDetection.setPadding(new Insets(12, 20, 12, 15));
        Text ObjectDetectLabel = new Text("Object Detection");
        ObjectDetectLabel.setFill(Color.rgb(219,205,205));
        Circle radioObjectDetect = new Circle(10);
        if(objectDetectionType){
            radioObjectDetect.setFill(Color.rgb(89, 227, 149));
        }else{
            radioObjectDetect.setFill(Color.rgb(45, 43, 43));
        }
        radioObjectDetect.setStroke(Color.rgb(219,205,205));
        radioObjectDetect.setStrokeWidth(2);
        objectDetection.setSpacing(50);
        Region spacer1 = new Region();
        HBox.setHgrow(spacer1, Priority.ALWAYS);
        objectDetection.getChildren().addAll(ObjectDetectLabel,spacer1, radioObjectDetect);

        // radio button to chose if you want classification
        HBox classification = new HBox();
        classification.setPadding(new Insets(12, 20, 12, 15));
        Text classificationLabel = new Text("Classification");
        classificationLabel.setFill(Color.rgb(219,205,205));
        Circle radioClassification = new Circle(10);
        if(classificationType){
            radioClassification.setFill(Color.rgb(89, 227, 149));
        }else{
            radioClassification.setFill(Color.rgb(45, 43, 43));
        }
        radioClassification.setStroke(Color.rgb(219,205,205));
        radioClassification.setStrokeWidth(2);
        Region spacer2 = new Region();
        HBox.setHgrow(spacer2, Priority.ALWAYS);
        classification.getChildren().addAll(classificationLabel,spacer2, radioClassification);
        classification.setSpacing(50);
        dType.getChildren().addAll(objectDetection, classification);
        dType.setBackground(new Background(new BackgroundFill(Color.rgb(45, 43, 43), CornerRadii.EMPTY, Insets.EMPTY)));

        // title and container of the output type
        VBox outputType = new VBox();
        Text outTypeTitle = new Text("Output Type");
        outTypeTitle.setFill(Color.rgb(219,205,205));
        VBox outTypeContainer = new VBox();

        // label and check box to choose bounding boxes as an output
        HBox boundingBoxes = new HBox();
        boundingBoxes.setPadding(new Insets(12, 20, 12, 15));
        Text boundingBoxesText = new Text("Bounding Boxes");
        boundingBoxesText.setFill(Color.rgb(219,205,205));
        Rectangle checkBounding = new Rectangle(20, 20);
        if(boundingBoxesType){
            checkBounding.setFill(Color.rgb(89, 227, 149));
        }else{
            checkBounding.setFill(Color.rgb(45, 43, 43));
        }
        checkBounding.setStroke(Color.rgb(219,205,205));
        checkBounding.setStrokeWidth(2);
        Region spacer3 = new Region();
        HBox.setHgrow(spacer3, Priority.ALWAYS);
        boundingBoxes.setBackground(new Background(new BackgroundFill(Color.rgb(45, 43, 43), CornerRadii.EMPTY, Insets.EMPTY)));
        boundingBoxes.getChildren().addAll(boundingBoxesText, spacer3, checkBounding);


        // label and check box to choose masks as an output
        HBox masks = new HBox();
        masks.setPadding(new Insets(12, 20, 12, 15));
        Text masksText = new Text("Masks");
        masksText.setFill(Color.rgb(219,205,205));
        Rectangle checkMasks = new Rectangle(20, 20);
        if(masksType){
            checkMasks.setFill(Color.rgb(89, 227, 149));
        }else{
            checkMasks.setFill(Color.rgb(45, 43, 43));
        }
        checkMasks.setStroke(Color.rgb(219,205,205));
        checkMasks.setStrokeWidth(2);
        Region spacer4 = new Region();
        HBox.setHgrow(spacer4, Priority.ALWAYS);
        masks.setBackground(new Background(new BackgroundFill(Color.rgb(45, 43, 43), CornerRadii.EMPTY, Insets.EMPTY)));
        masks.getChildren().addAll(masksText, spacer4, checkMasks);

        Pane spacer5 = new Pane();
        spacer5.setMinHeight(25);
        outTypeContainer.getChildren().addAll(outTypeTitle, boundingBoxes, masks);
        outputType.getChildren().addAll(outTypeContainer);

        Pane spacer6 = new Pane();
        spacer6.setMinHeight(25);
        VBox calculatedData =  new VBox();
        calculatedData.setPadding(new Insets(12, 20, 12, 15));

        // total images to be taken display
        HBox total = new HBox();
        Text totalText = new Text("Total Images To Be Taken:");
        totalText.setFill(Color.rgb(219,205,205));
        Text totalNumber = new Text(Integer.toString(totalImagesToTake));
        totalNumber.setFill(Color.rgb(219,205,205));
        Region spacer7 = new Region();
        HBox.setHgrow(spacer7, Priority.ALWAYS);
        total.getChildren().addAll(totalText, spacer7, totalNumber);


        Pane spacer9 = new Pane();
        spacer9.setMinHeight(25);

        // time remaining display
        HBox timePane = new HBox();
        Text timeText = new Text("Time Remaining");
        timeText.setFill(Color.rgb(219,205,205));
        Text hour = new Text(Integer.toString(hours) + ": ");
        Text minute = new Text(Integer.toString((int)minutes));
        hour.setFill(Color.rgb(219,205,205));
        minute.setFill(Color.rgb(219,205,205));
        Region spacer8 = new Region();
        HBox.setHgrow(spacer8, Priority.ALWAYS);
        timePane.getChildren().addAll(timeText, spacer8, hour, minute);

        calculatedData.getChildren().addAll(total, spacer9 ,timePane);

        otherDataInfo.getChildren().addAll(typeTitle, dType, spacer5, outputType, spacer6, calculatedData);

        checkBounding.setOnMouseClicked(e->{
            if(checkBounding.getFill().equals(Color.rgb(45, 43, 43))){
                checkBounding.setFill(Color.rgb(89, 227, 149));
                boundingBoxesType = true;
            }else{
                checkBounding.setFill(Color.rgb(45, 43, 43));
                boundingBoxesType = false;
            }
        });

        checkMasks.setOnMouseClicked(e->{
            if(checkMasks.getFill().equals(Color.rgb(45, 43, 43))){
                checkMasks.setFill(Color.rgb(89, 227, 149));
                masksType = true;
            }else{
                checkMasks.setFill(Color.rgb(45, 43, 43));
                masksType = false;
            }
        });

        radioObjectDetect.setOnMouseClicked(e->{
            radioObjectDetect.setFill(Color.rgb(89, 227, 149));
            radioClassification.setFill(Color.rgb(45, 43, 43));
            objectDetectionType = true;
            classificationType = false;
        });

        radioClassification.setOnMouseClicked(e->{
            radioClassification.setFill(Color.rgb(89, 227, 149));
            radioObjectDetect.setFill(Color.rgb(45, 43, 43));
            objectDetectionType = false;
            classificationType = true;
        });

        // each of the "thou" buttons darken the others when clicked
        oneThou.setOnMouseClicked(e->{
            imagesToTake = 1000;
            oneThou.setBackground(new Background(new BackgroundFill(Color.rgb(89, 227, 149), CornerRadii.EMPTY, Insets.EMPTY)));
            fiveThou.setBackground(new Background(new BackgroundFill(Color.rgb(45, 43, 43), CornerRadii.EMPTY, Insets.EMPTY)));
            tenThou.setBackground(new Background(new BackgroundFill(Color.rgb(45, 43, 43), CornerRadii.EMPTY, Insets.EMPTY)));
            fifteenThou.setBackground(new Background(new BackgroundFill(Color.rgb(45, 43, 43), CornerRadii.EMPTY, Insets.EMPTY)));
            totalImagesToTake = imagesToTake * numberOfSpecimens;
            hours = totalImagesToTake / 30 / 60 / 60;
            minutes = (((float) totalImagesToTake / 30 / 60 / 60) - hours) * 60;
            totalNumber.setText(Integer.toString(totalImagesToTake));
            hour.setText(Integer.toString(hours)+ ": ");
            minute.setText(Integer.toString((int)minutes));
        });
        fiveThou.setOnMouseClicked(e->{
            imagesToTake = 5000;
            fiveThou.setBackground(new Background(new BackgroundFill(Color.rgb(89, 227, 149), CornerRadii.EMPTY, Insets.EMPTY)));
            oneThou.setBackground(new Background(new BackgroundFill(Color.rgb(45, 43, 43), CornerRadii.EMPTY, Insets.EMPTY)));
            tenThou.setBackground(new Background(new BackgroundFill(Color.rgb(45, 43, 43), CornerRadii.EMPTY, Insets.EMPTY)));
            fifteenThou.setBackground(new Background(new BackgroundFill(Color.rgb(45, 43, 43), CornerRadii.EMPTY, Insets.EMPTY)));
            totalImagesToTake = imagesToTake * numberOfSpecimens;
            hours = totalImagesToTake / 30 / 60 / 60;
            minutes = (((float) totalImagesToTake / 30 / 60 / 60) - hours) * 60;
            totalNumber.setText(Integer.toString(totalImagesToTake));
            hour.setText(Integer.toString(hours)+ ": ");
            minute.setText(Integer.toString((int)minutes));
        });
        tenThou.setOnMouseClicked(e->{
            imagesToTake = 10000;
            tenThou.setBackground(new Background(new BackgroundFill(Color.rgb(89, 227, 149), CornerRadii.EMPTY, Insets.EMPTY)));
            fiveThou.setBackground(new Background(new BackgroundFill(Color.rgb(45, 43, 43), CornerRadii.EMPTY, Insets.EMPTY)));
            oneThou.setBackground(new Background(new BackgroundFill(Color.rgb(45, 43, 43), CornerRadii.EMPTY, Insets.EMPTY)));
            fifteenThou.setBackground(new Background(new BackgroundFill(Color.rgb(45, 43, 43), CornerRadii.EMPTY, Insets.EMPTY)));
            totalImagesToTake = imagesToTake * numberOfSpecimens;
            hours = totalImagesToTake / 30 / 60 / 60;
            minutes = (((float) totalImagesToTake / 30 / 60 / 60) - hours) * 60;
            totalNumber.setText(Integer.toString(totalImagesToTake));
            hour.setText(Integer.toString(hours)+ ": ");
            minute.setText(Integer.toString((int)minutes));
        });
        fifteenThou.setOnMouseClicked(e->{
            imagesToTake = 15000;
            fifteenThou.setBackground(new Background(new BackgroundFill(Color.rgb(89, 227, 149), CornerRadii.EMPTY, Insets.EMPTY)));
            fiveThou.setBackground(new Background(new BackgroundFill(Color.rgb(45, 43, 43), CornerRadii.EMPTY, Insets.EMPTY)));
            tenThou.setBackground(new Background(new BackgroundFill(Color.rgb(45, 43, 43), CornerRadii.EMPTY, Insets.EMPTY)));
            oneThou.setBackground(new Background(new BackgroundFill(Color.rgb(45, 43, 43), CornerRadii.EMPTY, Insets.EMPTY)));
            totalImagesToTake = imagesToTake * numberOfSpecimens;
            hours = totalImagesToTake / 30 / 60 / 60;
            minutes = (((float) totalImagesToTake / 30 / 60 / 60) - hours) * 60;
            totalNumber.setText(Integer.toString(totalImagesToTake));
            hour.setText(Integer.toString(hours)+ ": ");
            minute.setText(Integer.toString((int)minutes));
        });

        // enables the "Thou" button you clicked to still be green when you come back
        numberOfImages.parentProperty().addListener(e->{
            if(imagesToTake == 1000){
                oneThou.setBackground(new Background(new BackgroundFill(Color.rgb(89, 227, 149), CornerRadii.EMPTY, Insets.EMPTY)));
            }else if(imagesToTake == 5000){
                fiveThou.setBackground(new Background(new BackgroundFill(Color.rgb(89, 227, 149), CornerRadii.EMPTY, Insets.EMPTY)));
            }else if(imagesToTake == 10000){
                tenThou.setBackground(new Background(new BackgroundFill(Color.rgb(89, 227, 149), CornerRadii.EMPTY, Insets.EMPTY)));
            }else if(imagesToTake == 15000){
                fifteenThou.setBackground(new Background(new BackgroundFill(Color.rgb(89, 227, 149), CornerRadii.EMPTY, Insets.EMPTY)));
            }


        });

        // handles adding a class to the list of classes
        addClass.setOnAction(e ->{

            cDark.getChildren().clear();
            String name = className.getText();
            String number = speciemenNumber.getText();
            String[] both = new String[3];
            both[0] = name; // name of the class
            both[1] = number; // how many specimens
            both[2] = "0"; // how many have been imaged

            int index = 0;
            for(String[] individualClass: classesArray) {

                if (individualClass == null) {
                    classesArray[index] = both;
                    break;
                }
                index ++;
            }

            System.out.println(name +  number);

            index = 0;
            numberOfSpecimens = 0;
            for(String[] individualClass: classesArray) {

                if (individualClass != null) {
                    System.out.println(individualClass);
                    numberOfSpecimens = numberOfSpecimens + Integer.parseInt(individualClass[1]);
                    HBox individualClassContainer = new HBox();
                    Label ICCName = new Label(individualClass[0]);
                    ICCName.setTextFill(Color.rgb(219,205,205));
                    Label ICCNumber = new Label(individualClass[1]);
                    ICCNumber.setTextFill(Color.rgb(219,205,205));
                    ICCNumber.setAlignment(Pos.CENTER_RIGHT);
                    Region region1 = new Region();
                    HBox.setHgrow(region1, Priority.ALWAYS);
                    individualClassContainer.setSpacing(100);
                    individualClassContainer.getChildren().addAll(ICCName, region1, ICCNumber);
                    cDark.getChildren().addAll(individualClassContainer);
                    index++;
                }

            }
            totalImagesToTake = imagesToTake * numberOfSpecimens;
            hours = totalImagesToTake / 30 / 60 / 60;
            minutes = (((float) totalImagesToTake / 30 / 60 / 60) - hours) * 60;
            totalNumber.setText(Integer.toString(totalImagesToTake));
            hour.setText(Integer.toString(hours)+ ": ");
            minute.setText(Integer.toString((int)minutes));
            updateList.set(true);



        });

        // same as above but remove
        removeClass.setOnAction(e->{

            cDark.getChildren().clear();
            int index = 0;
            for(String[] individualClass: classesArray) {

                if (individualClass == null && index > 0) {
                    classesArray[index -1 ] = null;
                    break;
                }
                index ++;


            }
            index = 0;
            numberOfSpecimens = 0;
            for(String[] individualClass: classesArray) {

                if (individualClass != null) {
                    numberOfSpecimens = numberOfSpecimens + Integer.parseInt(individualClass[1]);
                    System.out.println(individualClass);
                    HBox individualClassContainer = new HBox();
                    Label ICCName = new Label(individualClass[0]);
                    ICCName.setTextFill(Color.rgb(219,205,205));
                    Label ICCNumber = new Label(individualClass[1]);
                    ICCNumber.setTextFill(Color.rgb(219,205,205));
                    Region region1 = new Region();
                    HBox.setHgrow(region1, Priority.ALWAYS);
                    individualClassContainer.setSpacing(100);
                    individualClassContainer.getChildren().addAll(ICCName, region1, ICCNumber);
                    cDark.getChildren().addAll(individualClassContainer);
                    index++;
                }

            }

            totalImagesToTake = imagesToTake * numberOfSpecimens;
            hours = totalImagesToTake / 30 / 60 / 60;
            minutes = (((float) totalImagesToTake / 30 / 60 / 60) - hours) * 60;
            totalNumber.setText(Integer.toString(totalImagesToTake));
            hour.setText(Integer.toString(hours)+ ": ");
            minute.setText(Integer.toString((int)minutes));
            updateList.set(true);

        });

        // updates the array when classes change
        classes.parentProperty().addListener(e ->{
            for(String[] individualClass: classesArray) {

                if (individualClass != null) {
                    System.out.println(individualClass);
                    HBox individualClassContainer = new HBox();
                    Label ICCName = new Label(individualClass[0]);
                    ICCName.setTextFill(Color.rgb(219,205,205));
                    Label ICCNumber = new Label(individualClass[1]);
                    ICCNumber.setTextFill(Color.rgb(219,205,205));
                    Region region1 = new Region();
                    HBox.setHgrow(region1, Priority.ALWAYS);
                    individualClassContainer.setSpacing(100);
                    individualClassContainer.getChildren().addAll(ICCName, region1, ICCNumber);
                    cDark.getChildren().addAll(individualClassContainer);
                }

            }
        });

        // adds all the panes to the grid
        grid.add(datasetName, 0, 0);
        grid.add(classes, 0, 2);
        grid.add(numberOfImages, 2, 0);
        grid.add(otherDataInfo, 2, 2);
        return grid;

    }

    // thou buttons
    public BorderPane numberSelection(String number){

        BorderPane select = new BorderPane();
        Text displayedNumber = new Text(number);
        displayedNumber.setFill(Color.rgb(219,205,205));
        select.setMaxHeight(56);
        select.setMinWidth(100);
        select.setBackground(new Background(new BackgroundFill(Color.rgb(45, 43, 43), CornerRadii.EMPTY, Insets.EMPTY)));

        select.backgroundProperty().addListener(e->{
            Color color = (Color) select.getBackground().getFills().get(0).getFill();
            if(color.equals(Color.rgb(89, 227, 149)) ){
                displayedNumber.setFill(Color.rgb(45, 43, 43));
            }else{
                displayedNumber.setFill(Color.rgb(219,205,205));
            }
        });

        select.setCenter(displayedNumber);

        return select;
    }

    // very simple grid to configure to the rul of the robot
    public GridPane robotConfig(){

        GridPane grid = new GridPane();
        grid.setMaxWidth(1000);
        InnerShadow gridShadow = new InnerShadow(10, -5, 0, Color.BLACK);
        grid.setEffect(gridShadow);
        grid.setBackground(new Background(new BackgroundFill(Color.rgb(55, 55, 55), CornerRadii.EMPTY, Insets.EMPTY)));
        BorderPane.setAlignment(grid,Pos.CENTER_LEFT);
        grid.setVgap(5);
        grid.setHgap(5);

        HBox connect = new HBox();
        connect.setPadding(new Insets(35, 15, 15, 35));
        connect.setAlignment(Pos.CENTER_LEFT);
        HBox connectDark = new HBox();
        connectDark.setPadding(new Insets(15, 15, 15, 15));
        connectDark.setBackground(new Background(new BackgroundFill(Color.rgb(45, 43, 43), CornerRadii.EMPTY, Insets.EMPTY)));
        connectDark.setSpacing(20);
        TextField url = new TextField("http://localhost:5000/status");
        Button submit = new Button("Ping robot");
        url.setMinWidth(200);
        connectDark.getChildren().addAll(url, submit);
        connect.getChildren().addAll(connectDark);

        submit.setOnAction(e->{
            url.getText();
            if(ping()){
                robotName.set("AILU-0001 ready");
            }else{
                robotName.set("AILU-0001 not ready");
            }
        });

        grid.add(connect, 1, 1);

        return grid;

    }


    // gridPane to control the robot.
    public GridPane robotControls(){

        GridPane grid = new GridPane();
        grid.setMaxWidth(1000);
        InnerShadow gridShadow = new InnerShadow(10, -5, 0, Color.BLACK);
        grid.setEffect(gridShadow);
        grid.setBackground(new Background(new BackgroundFill(Color.rgb(55, 55, 55), CornerRadii.EMPTY, Insets.EMPTY)));
        BorderPane.setAlignment(grid,Pos.CENTER_LEFT);
        grid.setVgap(5);
        grid.setHgap(5);

        BorderPane goTo = new BorderPane();
        goTo.setPadding(new Insets(35, 15, 15, 35));
        VBox goToContainer = new VBox();
        HBox goToVertictal = new HBox();
        goToVertictal.setSpacing(10);
        goToContainer.setPadding(new Insets(15, 15, 15, 15));
        goToContainer.setBackground(new Background(new BackgroundFill(Color.rgb(45, 43, 43), CornerRadii.EMPTY, Insets.EMPTY)));
        goToContainer.setSpacing(20);
        Label goToText = new Label("Set Camera Height in mm");
        goToText.setTextFill(Color.rgb(219,205,205));
        TextField position = new TextField(Integer.toString(vLimit.get()));
        Button submitVertical = new Button("go");
        position.setMinWidth(200);
        goToVertictal.getChildren().addAll(position, submitVertical);
        Button setZero = new Button("Set Height as Lower Limit");

        HBox currentBottomLimitCont = new HBox();
        currentBottomLimitCont. setSpacing(20);
        Text currentBottomLimitText = new Text("Current Limit: " + vLimit.get());
        currentBottomLimitText.setFill(Color.rgb(219,205,205));
        Text currentBottomLimit = new Text();
        currentBottomLimit.setFill(Color.rgb(219,205,205));
        currentBottomLimitCont.getChildren().addAll(currentBottomLimitText, currentBottomLimit);


        goToContainer.getChildren().setAll(goToVertictal, setZero, currentBottomLimitCont);
        goTo.setTop(goToText);
        goTo.setCenter(goToContainer);

        BorderPane rotateTo = new BorderPane();
        rotateTo.setPadding(new Insets(35, 15, 15, 35));
        VBox rotateToContainer = new VBox();
        HBox rotateToControls = new HBox();
        rotateToControls.setSpacing(10);
        rotateToContainer.setPadding(new Insets(15, 15, 15, 15));
        rotateToContainer.setBackground(new Background(new BackgroundFill(Color.rgb(45, 43, 43), CornerRadii.EMPTY, Insets.EMPTY)));
        rotateToContainer.setSpacing(20);
        Label rotateToText = new Label("Set Platform rotation in degrees");
        rotateToText.setTextFill(Color.rgb(219,205,205));
        TextField degrees = new TextField(Integer.toString(hLimit.get()));
        Button submitRotate = new Button("go");
        degrees.setMinWidth(200);
        rotateToControls.getChildren().addAll(degrees, submitRotate);
        Button setRotateLimit = new Button("Set Angle as Rotation Limit");
        HBox currentRotationLimitCont = new HBox();
        currentRotationLimitCont. setSpacing(20);
        Text currentRotationLimitText = new Text("Current Limit: " + hLimit.get());
        currentRotationLimitText.setFill(Color.rgb(219,205,205));
        Text currentRotationLimit = new Text();
        currentRotationLimit.setFill(Color.rgb(219,205,205));
        currentRotationLimitCont.getChildren().addAll(currentRotationLimitText, currentRotationLimit);
        rotateToContainer.getChildren().setAll(rotateToControls, setRotateLimit, currentRotationLimitCont);
        rotateTo.setTop(rotateToText);
        rotateTo.setCenter(rotateToContainer);

        VBox track = new VBox();
        track.setPadding(new Insets(35, 15, 15, 35));
        HBox trackContainer =  new HBox();
        Label trackLabel = new Label("Track Object With Camera");
        trackLabel.setTextFill(Color.rgb(219,205,205));
        Rectangle checkTrack = new Rectangle();
        checkTrack.setHeight(20);
        checkTrack.setWidth(20);
        checkTrack.setStroke(Color.rgb(219,205,205));
        if(trackObject.get()){
            checkTrack.setFill(Color.rgb(89, 227, 149));
        }else{
            checkTrack.setFill(Color.rgb(45, 43, 43));
        }

        checkTrack.setStrokeWidth(2);
        trackContainer.setSpacing(75);
        trackContainer.setBackground(new Background(new BackgroundFill(Color.rgb(45, 43, 43), CornerRadii.EMPTY, Insets.EMPTY)));
        trackContainer.setPadding(new Insets(15, 15, 15, 15));
        trackContainer.getChildren().addAll(trackLabel, checkTrack);
        track.getChildren().addAll(trackContainer);

        BorderPane lightsSettings = new BorderPane();
        lightsSettings.setPadding(new Insets(25, 15, 15, 15));
        lightsSettings.setMinWidth(400);
        lightsSettings.setMaxHeight(190);
        Text lightsText = new Text("Lights Settings");
        lightsText.setFill(Color.rgb(219,205,205));
        VBox lightsControls = new VBox();
        lightsControls.setBackground(new Background(new BackgroundFill(Color.rgb(45, 43, 43), CornerRadii.EMPTY, Insets.EMPTY)));

        HBox oneAtATime = new HBox();
        oneAtATime.setPadding(new Insets(11, 15, 11, 15));
        Label oneLabel = new Label("Only one light on at a time");
        oneLabel.setTextFill(Color.rgb(219,205,205));
        Circle oneRadio = radioCheck();
        if(lightsSettingsProp.get() == 2){
            oneRadio.setFill(Color.rgb(89, 227, 149));
        }
        Region oneSpacer = new Region();
        HBox.setHgrow(oneSpacer, Priority.ALWAYS);
        oneAtATime.getChildren().addAll(oneLabel,oneSpacer, oneRadio);
        lightsControls.getChildren().addAll(oneAtATime);

        HBox bothOn = new HBox();
        bothOn.setPadding(new Insets(11, 15, 11, 15));
        Label bothLabel = new Label("Both lights always on");
        bothLabel.setTextFill(Color.rgb(219,205,205));
        Circle bothRadio = radioCheck();
        if(lightsSettingsProp.get() == 1){
            bothRadio.setFill(Color.rgb(89, 227, 149));
        }
        Region bothSpacer = new Region();
        HBox.setHgrow(bothSpacer, Priority.ALWAYS);
        bothOn.getChildren().addAll(bothLabel, bothSpacer, bothRadio);
        lightsControls.getChildren().addAll(bothOn);

        HBox randomizeLights = new HBox();
        randomizeLights.setPadding(new Insets(11, 15, 11, 15));
        Label randLabel = new Label("Randomize lighting");
        randLabel.setTextFill(Color.rgb(219,205,205));
        Circle randRadio = radioCheck();
        if(lightsSettingsProp.get() == 3){
            randRadio.setFill(Color.rgb(89, 227, 149));
        }
        Region randSpacer = new Region();
        HBox.setHgrow(randSpacer, Priority.ALWAYS);
        randomizeLights.getChildren().addAll(randLabel, randSpacer, randRadio);
        lightsControls.getChildren().addAll(randomizeLights);

        lightsSettings.setTop(lightsText);
        lightsSettings.setCenter(lightsControls);

        BorderPane quickCheckContainer = new BorderPane();
        quickCheckContainer.setPadding(new Insets(200, 15, 15, 300));
        BorderPane quickCheckPane = new BorderPane();
        quickCheckPane.setPadding(new Insets(15, 15, 15, 15));
        quickCheckPane.setMaxWidth(200);
        quickCheckPane.setMaxHeight(45);
        quickCheckPane.setBackground(new Background(new BackgroundFill(Color.rgb(55, 55, 55), CornerRadii.EMPTY, Insets.EMPTY)));
        quickCheckPane.setBorder(new Border(new BorderStroke(Color.rgb(89, 227, 149),BorderStrokeStyle.SOLID, CornerRadii.EMPTY, BorderWidths.DEFAULT)));
        Text quickCheckText = new Text("Run Quick Check");
        quickCheckText.setFill(Color.rgb(219,205,205));
        BorderPane.setAlignment(quickCheckText,Pos.CENTER);
        quickCheckPane.setCenter(quickCheckText);
        quickCheckContainer.setCenter(quickCheckPane);


        grid.add(goTo, 0, 0);
        grid.add(rotateTo, 0, 1);
        grid.add(track, 0, 2);
        grid.add(lightsSettings, 2, 0);
        grid.add(quickCheckContainer, 2, 1);

        // event handlers for the go-to and rotate to panes
        submitVertical.setOnAction(e->{
            setToSever("goVe", Integer.parseInt(position.getText()));
        });
        setZero.setOnAction(e->{
            vLimit.set(Integer.parseInt(position.getText()));
            setToSever("Vlim", vLimit.get());
            currentBottomLimitText.setText("Current Limit :"+position.getText());
        });

        submitRotate.setOnAction(e->{
            setToSever("goHo", Integer.parseInt(degrees.getText()));
        });
        setRotateLimit.setOnAction(e->{
            hLimit.set(Integer.parseInt(degrees.getText()));
            setToSever("Hlim", hLimit.get());
            currentRotationLimitText.setText("Current Limit: "+degrees.getText());
        });
        checkTrack.setOnMouseClicked(e->{
            int value = 0;
            if(checkTrack.getFill().equals(Color.rgb(45, 43, 43))){
                checkTrack.setFill(Color.rgb(89, 227, 149));
                trackObject.set(true);
                value = 1;
            }else{
                checkTrack.setFill(Color.rgb(45, 43, 43));
                trackObject.set(false);
            }
            setToSever("trac", value);


        });
        oneRadio.setOnMouseClicked(e->{
            bothRadio.setFill(Color.rgb(45, 43, 43));
            randRadio.setFill(Color.rgb(45, 43, 43));
            oneRadio.setFill(Color.rgb(89, 227, 149));
            lightsSettingsProp.set(2);
            setToSever("ligh", lightsSettingsProp.get());

        });
        bothRadio.setOnMouseClicked(e->{
            oneRadio.setFill(Color.rgb(45, 43, 43));
            randRadio.setFill(Color.rgb(45, 43, 43));
            bothRadio.setFill(Color.rgb(89, 227, 149));
            lightsSettingsProp.set(1);
            setToSever("ligh", lightsSettingsProp.get());

        });
        randRadio.setOnMouseClicked(e->{
            oneRadio.setFill(Color.rgb(45, 43, 43));
            bothRadio.setFill(Color.rgb(45, 43, 43));
            randRadio.setFill(Color.rgb(89, 227, 149));
            lightsSettingsProp.set(3);
            setToSever("ligh", lightsSettingsProp.get());

        });

        quickCheckPane.setOnMouseEntered(e->{
            quickCheckPane.setBackground(new Background(new BackgroundFill(Color.rgb(45, 43, 43), CornerRadii.EMPTY, Insets.EMPTY)));
        });
        quickCheckPane.setOnMouseExited(e->{
            quickCheckPane.setBackground(new Background(new BackgroundFill(Color.rgb(55, 55, 55), CornerRadii.EMPTY, Insets.EMPTY)));
        });
        quickCheckPane.setOnMouseClicked(e->{
            run("test");
        });



        return grid;

    }

    public Circle radioCheck(){

        Circle box = new Circle(10);
        box.setStroke(Color.rgb(219,205,205));
        box.setFill(Color.rgb(45, 43, 43));
        box.setStrokeWidth(2);
        return box;

    }

    // sends a get request to the server and send true if the server answers
    public boolean ping(){
        try{
            String statusUrl = serverURL + "status";
            URL url = new URL(statusUrl);
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setDoOutput(true);
            connection.setRequestMethod("GET");
            connection.setRequestProperty("Accept", "application/json");


            if (connection.getResponseCode() != 201) {
                System.out.println("connection failed");
                return false;
            }
            BufferedReader br = new BufferedReader(new InputStreamReader((connection.getInputStream())));

            String responce;
            System.out.println("Output from Server .... \n");
            while ((responce = br.readLine()) != null) {
                System.out.println(responce);
            }

            connection.disconnect();
            return true;

        }catch (ConnectException err){
            return false;
        }
        catch (MalformedURLException err) {

            err.printStackTrace();
            return false;

        }catch (IOException err) {

            err.printStackTrace();
            return false;

        }

    }

    public static void main(String[] args) {
        launch(args);
    }
}


