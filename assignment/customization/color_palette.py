import requests
from requests.structures import CaseInsensitiveDict
import json

color_codes = {
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "purple": (76, 0, 153),
    "violet": (153, 0, 153),
    "brown": (165, 42, 42),
    "orange": (255, 128, 0),
}


# input the favourite color of the child
def get_theme(red, green, blue):
    url = "http://colormind.io/api/"
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/x-www-form-urlencoded"
    data = '{"input":[[' + str(red) + ',' + str(green) + ',' + str(blue) + '],"N","N","N"],"model":"default"}'
    response = requests.post(url, headers=headers, data=data)
    returned_colors = ""
    if response.status_code == 200:
        returned_colors = json.loads(response.text)["result"][3]
    return returned_colors


def generate_colors(fav_color):
    base_color_code = color_codes[fav_color]
    alr = get_theme(*base_color_code)
    print(alr)


if __name__ == "__main__":
    generate_colors()
