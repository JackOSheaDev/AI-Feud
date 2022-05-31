import json
import os
import random
import string
from cognitive_vision import CognitiveVision
from dotenv import load_dotenv

load_dotenv()


class GuessBackend:
    characters = string.ascii_letters + string.digits

    def __init__(self):
        self.cv = CognitiveVision(key=os.getenv("SUBSCRIPTION_KEY"),
                                  endpoint=os.getenv("ENDPOINT"))
        self.current_image_url = self.generate_url()

    @property
    def current_image_url(self):
        return self.__current_image_url

    @current_image_url.setter
    def current_image_url(self, image_dict):
        self.__current_image_url = image_dict

    def generate_url(self):
        # get random password pf length 8 with letters, digits, and symbols

        password = ''.join(random.choice(self.characters) for i in range(25))

        generated_value = password
        return {"url": f"https://picsum.photos/seed/{generated_value}picsum/200/300"}

    def scan_image(self):
        return self.cv.call_cognitive_vision(self.current_image_url)

if __name__ == "__main__":
    gb = GuessBackend()
    print(gb.current_image_url)
    #print(gb.scan_image())
    contents = [tag['name'] for tag in gb.scan_image()[0]]
    main_dict = {"Url": gb.current_image_url["url"], "Caption": gb.scan_image()[1], "Contents": contents[0:6]}

    main_dict = json.dumps(main_dict)
    print(main_dict)

