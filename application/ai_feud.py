"""
Purpose: To create a GUI using Kivy for a game named AI Feud.
Author: Jack O'Shea
Date: 17/06/2022

"""

# JSON Module to load in cached values for the GUI to use.
import json
# Random module to choose a random value out of the cached values.
from random import randint
# Kivy App modules which are used for the application for the GUI.
from kivy.app import App
from kivy.core.text import LabelBase
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, NoTransition, Screen
from kivy.uix.textinput import TextInput

# Custom Fonts being used by the project. Anton used for headings and NotoEmoji used for Emojis.
LabelBase.register(name='Anton', fn_regular=r'../resources/Anton-Regular.ttf')
LabelBase.register(name='Emoji_Font', fn_regular=r'../resources/NotoEmoji-VariableFont_wght.ttf')


# Function which opens results file and gets the contents into a dictionary.
def get_results():
    """
    A function which opens a file named results.json and returns the contents of the file as a dictionary.
    Returns
    -------
    file_data: dict
        A dictionary which contains all the cached values from the Cognitive Vision application.
    """

    with open(r"resources/results.json", "r+") as file:
        # Get dictionary.
        file_data = json.load(file)["Results"]
    # Return data.
    return file_data


# Main Application which implements the screen manager.
class AIFeud(App):
    """
    A class which is used to represent the AI Feud Application, it contains a screen manager to control the navigation.

    ...

    Attributes
    ----------
    screen_manager: ScreenManager
        The screen manager is a Kivy Object which is used to control the navigation between screens.

    Methods
    -------
    build()
        A function belonging to Kivy which initializes the application with the screen manager and parameters necessary.

    """

    def build(self):
        """
        Builds the application and returns it.

        Returns
        -------
        screen_manager: ScreenManager
            The manager for all the screens.
        """

        # Contains Game Data for the Program
        game_model = DataModel()

        # Create screen_manager and add widgets.
        screen_manager = ScreenManager(transition=NoTransition())
        screen_manager.add_widget(MainScreen(name="main"))
        screen_manager.add_widget(GameScreen(game_model, name="game"))

        # Return the screen_manager to start the application
        return screen_manager


# Main DataModel of the application used by classes to manipulate the data.
class DataModel:
    """

    A class which is used to represent the data model of the application, so it can be manipulated by the screens.

    ...

    Attributes
    ----------
    self.results: dict
        The return value of get_results() which reads in the contents of the file called results.json
    choice: dict element
        The current chosen result from results to use in the game.
    lives: int
        How many lives the player has before they lose the game
    image_url: str
        The link to the image which should be displayed to the user.
    correct_guess_count: int
        The number of correct guesses
    Methods
    -------
    __init__()
        Initialises the model object with its variables necessary for the program to function.
    choose_result()
        Chooses a random result from the dictionary to be used by the game.
    check_guess(text: str)
        Compares the guess to the contents of the dictionary to check if it is a valid guess.
    update_results()
        Used when resetting the view to reinitialise all the values.

    """

    # Class variable which represents the contents of the results.json file.
    results = get_results()

    def __init__(self):
        # The choice is a random selection from the results' dict.
        self.choice = self.choose_result()
        # Lives is the number of guesses a user receives.
        self.lives = 5
        # Image Url is the url to be used by the async image.
        self.image_url = self.choice['Url']
        self.correct_guess_count = 0

    def choose_result(self):
        """
        Chooses a result from the results' dict.

        Returns
        -------
        self.results[random_value]
            A random selection from the dictionary named results.

        """

        # Gets a random value between 0 and the number of items in the dictionary.
        random_value = randint(0, len(self.results) - 1)
        # Returns the random selection.
        return self.results[random_value]

    def check_guess(self, text):
        """
        Checks if the user enters a correct guess.

        Parameters
        ----------
        text
            The text entered by the user

        Returns
        -------
        True or False
            Whether the text is present in the list.
        """

        if text in self.choice['Contents']:
            return True
        else:
            self.lives = self.lives - 1
            return False

    def update_results(self):
        """
        Resets all the values of the model for a new round.

        Returns
        -------

        """

        self.choice = self.choose_result()
        self.lives = 5
        self.image_url = self.choice['Url']


# Main Screen used for login
class MainScreen(Screen):
    """
    A class which is used to represent the main screen of the game which the user starts the game with.

    Methods
    -------
    start
        Changes the view to the game screen.
    """

    def start(self):
        self.manager.current = "game"


# Game screen used for playing the game.
class GameScreen(Screen):
    """
        A class which is used to represent the game screen, it is one of the screens of the screen manager.
        ...

        Attributes
        ----------
        model: DataModel
            The data of the program which is used to change information on the view and control game logic.
        input_box: TextInput
            An input box widget used by the user to enter text.
        btn_reset: Button
            Used to reset the game.
        btn_quit: Button
            Used to quit the game.
        labels: dict
            The UI labels which are manipulated when the user makes a correct guess

        Methods
        -------
        add_input()
            Adds a text input to the screen.
        set_lives()
            Updates the life counter on the screen.
        set_image_used()
            Updates the image on the screen.
        set_labels()
            Adds Label elements to the screen.
        check(event)
            Check if the user enters a correct guess.
        end_game()
            Called when the user enters in all their guesses.
        reset()
            Resets the game so the user can play again.
        quit()
            Ends the game when the user enters all correct guesses.
        """

    def __init__(self, model, **kw):
        # Super constructor call
        super().__init__(**kw)
        # Data model which is referenced and manipulated by the program
        self.model = model

        # Input box which is loaded into UI.
        self.input_box = TextInput(hint_text='Enter Text',
                                   multiline=False,
                                   size_hint=(0.75, 0.3),
                                   pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                   font_size=20,
                                   on_text_validate=self.check
                                   )

        # Reset button which is loaded into UI.
        self.btn_reset = Button(text='Reset',
                                size_hint=(0.75, 0.25),
                                pos_hint={'center_x': 0.5, 'center_y': 0.15},
                                fontsize=40,
                                font_name='DejaVuSans',
                                background_normal='',
                                background_color='#00E8FC'
                                )

        # Quit button which is loaded into UI.
        self.btn_quit = Button(text='Quit',
                               size_hint=(0.75, 0.25),
                               pos_hint={'center_x': 0.5, 'center_y': 0.15},
                               fontsize=40,
                               font_name='DejaVuSans',
                               background_normal='',
                               background_color='#00E8FC'
                               )

        # Add the input element to the UI.
        self.add_input()
        # Set the lives on the screen.
        self.set_lives()
        # Set the image used on the screen.
        self.set_image_used()
        # Create an empty dictionary.
        self.labels = {}
        # Add labels to the display
        self.set_labels()

    def add_input(self):
        self.ids.main_box.add_widget(self.input_box)

    def set_lives(self):
        self.ids.life_counter.text = f"You have {self.model.lives} lives"

    def set_image_used(self):
        self.ids.image_used.source = self.model.image_url

    def set_labels(self):
        # Clear any widgets currently on the screen (used when the game is reset)
        self.ids.answers.clear_widgets()

        # Add labels to dictionary and then the screen.
        for index, element in enumerate(self.model.choice['Contents']):
            self.labels[element] = Label(text=str(index + 1),
                                         font_name='DejaVuSans',
                                         color='#00E8FC',
                                         font_size=30
                                         )
            self.ids.answers.add_widget(self.labels[element])

        # Print the labels to the console.
        print(self.labels)

    def check(self, event):
        print(f"Event Captured from button {event}")

        # Get text from input box and sanitize.
        text = self.input_box.text.strip().lower()
        # If the guess is correct.
        if self.model.check_guess(text):
            # Check if the label has already been set.
            if self.labels[text].text.lower() != text:
                # Add text to UI.
                self.labels[text].text = text.capitalize()
                self.model.correct_guess_count = self.model.correct_guess_count + 1
                if self.model.correct_guess_count == len(self.model.choice['Contents']):
                    self.end_game('congrats you won !')

            else:
                # Check to see if the label has already been set. This is here to add score functionality in future
                # update.
                pass
                print('Here')

        # If the guess is incorrect
        else:
            # Update lives on screen.
            self.set_lives()

            # If they have no more lives, end the game.
            if self.model.lives == 0:
                self.end_game()
        # Reset the input text box for convenience.
        self.input_box.text = ''

    def end_game(self, text='Thank you for playing !'):
        # 1. Show all results to the user.
        for key in self.labels.keys():
            self.labels[key].text = key

        # 2. Delete the text box.
        self.ids.main_box.remove_widget(self.input_box)

        # 3: Update Score Label
        self.ids.life_counter.text = text

        # 4. Add Button for restart
        self.btn_reset.bind(on_press=self.reset)
        self.ids.main_box.add_widget(self.btn_reset)

        # 5. Add button to quit
        self.btn_quit.bind(on_press=self.quit)
        self.ids.main_box.add_widget(self.btn_quit)

    def reset(self, event):
        print(f"Event Captured from button {event}")
        # 1. Remove the buttons from the screen.
        self.ids.main_box.remove_widget(self.btn_quit)
        self.ids.main_box.remove_widget(self.btn_reset)

        # 2. Re-add the input box.
        self.add_input()

        # 3. Set their lives back to 5
        self.model.lives = 5

        # 4. Get a new choice from the dictionary
        self.model.update_results()

        # 5. Refresh UI elements on the screen.
        self.set_lives()
        self.set_image_used()
        self.labels = {}
        self.set_labels()

    @staticmethod
    def quit(event):
        print(f"Event Captured from button {event}")
        # Exit the program
        quit()


if __name__ == "__main__":
    AIFeud().run()
