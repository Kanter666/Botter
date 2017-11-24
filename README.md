# Botter
Application for easy creation of bot enviroments. Aim is to cover image processing and controls in black box, that user can just call functions getScore() or getPosition(),.. without knowing how to use advanced libraries.

## Usage

### Record Game
First step for creating bot enviroment would be to record example game. This will allow user to select game screen position, location where he wants to save screens and also speed of screenshots (limited by users machine).

### Main window
This is the main screen of Botter where you can quickly create functions. 

![Alt text](./botterMain.png?raw=true "Main screen")

This screen has multiple features:
* selection of current screenshot
* list of default functions
* manage current functions(run, change, delete)
* add new function
* save current selection for later use
* select border image - for finding location of game screen - usually edge that is unique and always the same

The run function option will be run on selected screenshot if possible (you can't run hasChanged funcion on one screen,..). Here you can test if you selected good treshold for text recognition,..
![Alt text](./result.png?raw=true "Main screen")


### Create functions
This is pop-up window that shows when you press "Add function for box" button. 

![Alt text](./exampleFunction.png?raw=true "Example function")

Here you can choose different types of functions and tune their properties.


