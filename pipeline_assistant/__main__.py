import json
import os
import shutil
from xml.dom import minidom
from webexteamssdk import WebexTeamsAPI
from .webex.webex_helper import Webex_helper
from tabulate import tabulate

def main() -> None:  # pragma: no cover
    """
    The main function executes on commands:
    `python -m pipeline_assistant` or `$ pipeline_assistant `.
    """
    print("Creating Webex Teams API object")
    https_proxy = os.environ.get("WEBEX_HTTPS_PROXY")
    http_proxy = os.environ.get("WEBEX_HTTP_PROXY")
    custom_message = os.environ.get("WEBEX_CUSTOM_MESSAGE")

    xunit_path = os.environ.get("XUNIT_PATH")

    if https_proxy and http_proxy:
        api = WebexTeamsAPI(
            os.environ["WEBEX_TEAMS_ACCESS_TOKEN"],
            proxies={"https": https_proxy, "http": http_proxy},
        )
    elif https_proxy:
        api = WebexTeamsAPI(
            os.environ["WEBEX_TEAMS_ACCESS_TOKEN"],
            proxies={"https": https_proxy},
        )
    elif http_proxy:
        api = WebexTeamsAPI(
            os.environ["WEBEX_TEAMS_ACCESS_TOKEN"],
            proxies={"http": http_proxy},
        )
    else:
        api = WebexTeamsAPI(os.environ["WEBEX_TEAMS_ACCESS_TOKEN"])

    print(f"Hi, I am {api.people.me().displayName} !")
    helper = Webex_helper(api)
    people = json.loads(os.environ["WEBEX_PEOPLE"])
    rooms = json.loads(os.environ["WEBEX_ROOMS"])
    result_path = os.environ["RESULT_PATH"]
    print(f"Create rooms: {rooms}")
    available_rooms = helper.create_rooms(rooms)
    print(f"Subscribe people: {people}")
    helper.subscribe_people(people, available_rooms)
    print("Save result")
    archive = shutil.make_archive(result_path, "zip", result_path)
    print(f"Results saved as {archive}")

    if custom_message:
        message=custom_message
    else:
        message="New results available!"

    if xunit_path:
        message = format(xunit_path,message)

    for room in available_rooms:
        print(f"Send message to {room.title}")
        # Post a message to the new room, and upload a file
        api.messages.create(room.id, text=message, files=[archive])

def format(path,message):
    doc = minidom.parse(path)
    test_suites = doc.getElementsByTagName("testsuite")
    # Header for the table
    suite_name_header = 'Suite'
    tests_header = 'Total'
    failures_header = 'Failures'
    errors_header = 'Errors'
    skipped_header = 'Skipped'
    time_header = 'Time'
    headers = [suite_name_header, tests_header, failures_header, errors_header, skipped_header, time_header]
    # Table
    table = []
    for test_suite in test_suites:
        # use the test_suite attributes to generate a table row
        test_suite_name = test_suite.getAttribute("name")
        test_suite_tests = test_suite.getAttribute("tests")
        test_suite_failures = test_suite.getAttribute("failures")
        test_suite_errors = test_suite.getAttribute("errors")
        test_suite_skipped = test_suite.getAttribute("skipped")
        test_suite_time = test_suite.getAttribute("time")
        # create a table row
        row = [test_suite_name, test_suite_tests, test_suite_failures, test_suite_errors, test_suite_skipped, test_suite_time]
        table.append(row)
        formated_table = tabulate(table, headers=headers,tablefmt="github")
        message += "\n"+"```\n"+formated_table+"\n```"
    return message

if __name__ == "__main__":  # pragma: no cover
    main()
