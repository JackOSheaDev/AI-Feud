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
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, NoTransition, Screen


# Model of the MVC which contains the data needed for the GUI to run.
def get_results():
    """
    A function which opens a file named results.json and returns the contents of the file as a dictionary.
    Returns
    -------
    file_data: dict
        A dictionary which contains all the cached values from the Cognitive Vision application.
    """

    with open("results.json", "r+") as file:
        # Get dictionary.
        file_data = json.load(file)["Results"]
    # Return data.
    return file_data


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
        A function belonging to Kivy which initializes the application with the screen manager and parameters neccesary.

    """

    def build(self):
        """
        Builds the application and returns it.

        Returns
        -------
        screen_manager: ScreenManager
            The manager for all the screens.
        """

        # Create screen_manager and add widgets.
        screen_manager = ScreenManager(transition=NoTransition())
        screen_manager.add_widget(MainScreen(name="main"))
        screen_manager.add_widget(GameScreen(name="game"))

        return screen_manager


class MainScreen(Screen):
    def start(self):
        self.manager.current = "game"


class GameScreen(Screen):
    image_url = StringProperty()
    image_values = []
    value_list = []
    lives = 3

    def __init__(self, **kw):
        super().__init__(**kw)
        self.results = get_results()
        self.choice = self.choose_result()
        self.image_url = self.choice['Url']
        self.image_values = self.choice['Contents']

        self.value_list = [
            self.ids.image_value_1,
            self.ids.image_value_2,
            self.ids.image_value_3,
            self.ids.image_value_4,
            self.ids.image_value_5,
            self.ids.image_value_6,
        ]

        print(self.results)

    def get_lives(self):
        return f"You have {self.lives} lives"

    def choose_result(self):
        random_value = randint(0, len(self.results) - 1)
        return self.results[random_value]

    def check(self):
        text = self.ids.user_guess.text
        if text.strip().lower() in self.image_values:
            index = self.image_values.index(text.strip().lower())
            self.value_list[index].text = text
        self.ids.user_guess.text = ''
        print(text)


if __name__ == "__main__":
    AIFeud().run()
