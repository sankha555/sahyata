import requests
from requests.structures import CaseInsensitiveDict
import json

# input the favourite color of the child
def getTheme(red,green,blue):
    url = "http://colormind.io/api/"
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/x-www-form-urlencoded"
    data = '{"input":[[' + str(red) + ',' + str(green) + ',' + str(blue) + '],"N","N","N"],"model":"default"}'
    response = requests.post(url, headers=headers, data=data)
    returnedColors = ""
    if(response.status_code == 200):
        returnedColors = json.loads(response.text)["result"][3]
    return returnedColors

def main():
    alr = "Hello"
    print("Generating random colours")
    alr = getTheme(145,65,187)
    print(alr)

if __name__ == "__main__":
    main()

    