"""
Purpose: To create a class which implements cognitive_vision on random images.
Author: Jack O'Shea
Date: 31/05/2022

"""

# JSON module to change the dictionary into a JSON object.
import json
# OS used for environment variables.
import os
# Random to make a random string of characters.
import random
# String to import the characters needed for the string.
import string
# Import my cognitive_vision class.
from backend.cognitive_vision import CognitiveVision
# Dotenv to load in environmental variables to avoid releasing subscription key.
from dotenv import load_dotenv

# Load environmental variables.
load_dotenv()


class GuessBackend:
    """
        A class which is used to generate random images and return the results of image analysis.

        ...

        Attributes
        ----------
        cv: cognitive_vision
            The custom API interface class I created.
        current_image_url: str
            The randomly generated URL pointing to an image.

        Methods
        -------
        current_image_url()
            returns the current image url being used by the cognitive_vision class.
        current_image_url(image_dict)
            sets the value of the url.
        generate_url()
            generates a random url
        """

    # Characters to be used in the random string.
    characters = string.ascii_letters + string.digits

    def __init__(self):
        self.cv = CognitiveVision(key=os.getenv("SUBSCRIPTION_KEY"),
                                  endpoint=os.getenv("ENDPOINT"))
        self.current_image_url = self.generate_url()

    @property
    def current_image_url(self):
        """
        A function which returns the url of the current image.

        Returns
        -------
        The value of the current images url.
        """
        return self.__current_image_url

    @current_image_url.setter
    def current_image_url(self, image_dict):
        """
        Sets the current_image_url

        Parameters
        ----------
        image_dict
            The value you wish to assign to the url.

        Returns
        -------

        """
        self.__current_image_url = image_dict

    def generate_url(self):
        """
        Generates the url to a random image.

        Returns
        -------
        Returns a dictionary containing an url which is a random string.
        """

        # Makes a string 25 characters long of random characters.
        generated_value = ''.join(random.choice(self.characters) for _ in range(25))

        # Returns the Dictionary containing the URL.
        return {"url": f"https://picsum.photos/seed/{generated_value}picsum/200/300"}

    def scan_image(self):
        """
        Scans the image at the currently stored url.

        Returns
        -------
        The results of the call_cognitive_vision function.
        """
        # Scan the image stored at the current url.
        return self.cv.call_cognitive_vision(self.current_image_url)


if __name__ == "__main__":
    # Create an object for scanning the image.
    gb = GuessBackend()
    # Print the current URL
    print(gb.current_image_url)
    # Scan the image and return its caption.
    print(gb.scan_image()[1])

    # Parse it into a JSON object containing url, contents and caption.
    contents = [tag['name'] for tag in gb.scan_image()[0]]
    main_dict = {"Url": gb.current_image_url["url"], "Caption": gb.scan_image()[1], "Contents": contents[0:6]}

    with open("resources/results.json", "r+") as file:
        file_data = json.load(file)
        file_data["Results"].append(main_dict)
        file.seek(0)
        json.dump(file_data, file, indent=4)
