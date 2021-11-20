from server.connection import API_BASE_URL, make_post_request
from syslogs.logs import print_log


def student_details(details):
    name = details["name"]
    dob = details["dob"]
    traits = details["traits"]
    preferences = details["preferences"]

    url = API_BASE_URL + "student/registration"

    req = {
        "name": name,
        "dob": dob,
        "traits": traits,
        "preferences": preferences
    }

    res = make_post_request(url, req, True)
    if res.status_code == 201:
        student_info = res.json()

        lines = [student_info[key] for key in student_info.keys()]

        with open("student.txt", "w") as file:
            file.writelines(lines)
    else:
        print_log(res.error, "error")
