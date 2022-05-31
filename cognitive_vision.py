"""
Purpose: To create a class which functions as a connection to the azure cognitive API.
Author: Jack O'Shea
Date: 31/05/2022

"""

# JSON module to change the dictionary into a JSON object.
import json
# OS used for environment variables.
import os
# Requests used to make an API call.
import requests
# Dotenv to load in environmental variables to avoid releasing subscription key.
from dotenv import load_dotenv
load_dotenv()


class CognitiveVision:
    """
    A class which is used to represent the connection to the Azure Cognitive Vision API.

    ...

    Attributes
    ----------
    key: str
        The API Subscription key which must be used to verify your request.
    endpoint: str
        The API Endpoint which is the URL used by the request library.

    Methods
    -------
    key()
        returns the value of the key.
    key(subscription_key)
        allows a new key to be set.
    endpoint()
        returns the value of the endpoint.
    endpoint(endpoint)
        sets a new endpoint.
    call_cognitive_vision()
        used to perform analysis on an image or url passed.
    """

    def __init__(self, key, endpoint):
        """

        Parameters
        ----------
        key: str
            The API Subscription key which must be used to verify your request.
        endpoint: str
            The API Endpoint which is the URL used by the request library.
        """

        # Subscription Key.
        self.key = key
        # Endpoint for the REST API.
        self.endpoint = endpoint

    @property
    def key(self):
        """
        A function used to return the value of the subscription key.

        Returns
        -------
        key
            the subscription key currently set.
        """

        # Getter for the subscription key.
        return self.__key

    @key.setter
    def key(self, subscription_key):
        """
        A method used to set a new value for the subscription key.

        Parameters
        ----------
        subscription_key
            The value of the subscription key you wish to set.

        Raises
        ------
        ValueError
            Raised if the subscription key is not the correct length.
        TypeError
            If a data type other than a string is passed to the method.

        Returns
        -------
        No Return Value.
        """

        # Check if the key is 32 characters long and a string, otherwise raise exception.
        try:
            if len(subscription_key) == 32:
                self.__key = subscription_key
            else:
                raise ValueError

        # Handle Exceptions
        except TypeError:
            print("It appears you entered a value which is not a string for the key !")
        except ValueError:
            print("It appears your key is not the correct length for a subscription key")

    @property
    def endpoint(self):
        """
                A function used to return the value of the endpoint url.

                Returns
                -------
                endpoint
                    the endpoint URL used by the requests' module.
        """

        # Getter for the endpoint of REST API.
        return self.__endpoint

    @endpoint.setter
    def endpoint(self, endpoint):
        """
                A method used to set a new value for the endpoint.

                Parameters
                ----------
                endpoint
                    The value of the endpoint you wish to set.

                Raises
                ------
                ValueError
                    Raised if the endpoint does not contain the correct url.
                TypeError
                    If a data type other than a string is passed to the method.

                Returns
                -------
                No Return Value.
        """

        # Check if the endpoint contains the correct string, otherwise raise value error.
        try:
            if "cognitiveservices.azure.com/" in endpoint:
                self.__endpoint = endpoint + "vision/v3.1/analyze"
            else:
                raise ValueError

        # Handle Exceptions
        except TypeError:
            print("It appears you entered a value which is not a string for the endpoint")
        except ValueError:
            print("That does not look like a correct endpoint for the program")

    def call_cognitive_vision(self, input_file):
        """
        A method which performs azure cognitive vision on an image and returns the result.
        Parameters
        ----------
        input_file
            Either a URL stored in a dictionary or the path to an image.

        Returns
        -------
        analysis["tags"]
            The tags are what the AI believes is in the image.
        analysis["description"]
            The description is a sentence describing the image.
        """

        # Checks if it is a string or dictionary.
        if isinstance(input_file, str):
            # Open image and save it as bytes.
            with open(input_file, "rb") as input_image:
                image_data = input_image.read()
                # Set the correct content type for the API.
                content_type = "application/octet-stream"

        else:
            # Change the dictionary into a json file.
            image_data = json.dumps(input_file)
            # Set the correct content type.
            content_type = "application/json"

        # Subscription key and the content type which must be passed to the REST Api.
        headers = {'Ocp-Apim-Subscription-Key': self.key, 'Content-Type': content_type}
        # Optional Parameters you are requesting from the API.
        params = {'visualFeatures': 'Description,Tags,Objects'}

        # Get the response from the Azure Cognitive Vision API.
        response = requests.post(self.endpoint, headers=headers, params=params, data=image_data)
        # Check if the API returned a response.
        response.raise_for_status()
        # Parse the response into JSON.
        analysis = response.json()

        # Return list of dictionaries of returned values.
        return analysis["tags"], analysis["description"]["captions"][0]["text"].capitalize()


if __name__ == "__main__":
    # Initialise Cognitive Vision Object with key and endpoint.
    cv = CognitiveVision(key=os.getenv("SUBSCRIPTION_KEY"),
                         endpoint=os.getenv("ENDPOINT"))

    # Test API with image of dog.
    results, caption = cv.call_cognitive_vision("download.jpg")
    values2 = cv.call_cognitive_vision({"url": "https://i.picsum.photos/id/1053/200/300.jpg?hmac=g"
                                               "-MecQlcjGrVSsQX4Odc3D1ORJuzKsofZ6BIVb1Y4ok"})

    print(caption)
    for result in results:
        print(result["name"])
        print(result["confidence"])
