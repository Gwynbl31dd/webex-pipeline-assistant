from traceback import print_tb
from webexteamssdk import WebexTeamsAPI
from .webex.webex_helper import Webex_helper
import json
import os
import shutil

def main() -> None:  # pragma: no cover
    """
    The main function executes on commands:
    `python -m pipeline_assistant` or `$ pipeline_assistant `.
    """
    # Can use environment variables to set the API access token WEBEX_TEAMS_ACCESS_TOKEN
    print("Creating Webex Teams API object")
    https_proxy = os.environ.get("WEBEX_HTTPS_PROXY")
    http_proxy = os.environ.get("WEBEX_HTTP_PROXY")

    if https_proxy and http_proxy:
        api = WebexTeamsAPI(os.environ['WEBEX_TEAMS_ACCESS_TOKEN'],proxies={"https": https_proxy,"http": http_proxy})
    elif https_proxy:
        api = WebexTeamsAPI(os.environ['WEBEX_TEAMS_ACCESS_TOKEN'],proxies={"https": https_proxy})
    elif http_proxy:
        api = WebexTeamsAPI(os.environ['WEBEX_TEAMS_ACCESS_TOKEN'],proxies={"http": http_proxy})
    else:
         api = WebexTeamsAPI(os.environ['WEBEX_TEAMS_ACCESS_TOKEN'])

    print(f'Hi, I am {api.people.me().displayName} !')
    helper = Webex_helper(api)
    people = json.loads(os.environ['WEBEX_PEOPLE'])
    rooms = json.loads(os.environ['WEBEX_ROOMS'])
    result_path = os.environ['RESULT_PATH']
    print(f'Create rooms: {rooms}')
    available_rooms = helper.create_rooms(rooms)
    print(f'Subscribe people: {people}')
    helper.subscribe_people(people,available_rooms)
    print('Save result')
    archive = shutil.make_archive(result_path, 'zip', result_path)
    print(f'Results saved as {archive}')
    for room in available_rooms:
        print(f'Send message to {room.title}')
        # Post a message to the new room, and upload a file
        api.messages.create(room.id, text="New result available!",
                    files=[archive])

if __name__ == "__main__":  # pragma: no cover
    main()