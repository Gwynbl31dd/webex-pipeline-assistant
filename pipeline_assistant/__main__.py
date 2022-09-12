from traceback import print_tb
from webexteamssdk import WebexTeamsAPI
from .webex.webex_helper import Webex_helper
import json
import os
import shutil

def main() -> None:  # pragma: no cover
    """
    The main function executes on commands:
    `python -m pipeline_assistant` and `$ pipeline_assistant `.
    """
    print("Executing main function")
    # Can use environment variables to set the API access token WEBEX_TEAMS_ACCESS_TOKEN
    print("Creating Webex Teams API object")
    api = WebexTeamsAPI(os.environ['WEBEX_TEAMS_ACCESS_TOKEN'])
    print(f'Hi, I am {api.people.me().displayName} !')
    
    helper = Webex_helper(api)

    people = json.loads(os.environ['WEBEX_PEOPLE'])
    rooms = json.loads(os.environ['WEBEX_ROOMS'])
    result_path = os.environ['RESULT_PATH']

    print(f'People: {people}')
    print(f'Rooms: {rooms}')
    print(f'Result path: {result_path}')

    print('Create rooms')
    available_rooms = helper.create_rooms(rooms)
    print('Subscribe people')
    helper.subscribe_people(people,available_rooms)

    print('Save result')
    archive = shutil.make_archive(result_path, 'zip', result_path)
    print(f'Results saved as {archive}')

    for room in available_rooms:
        print(f'Send message to {room.title}')
        # Post a message to the new room, and upload a file
        api.messages.create(room.id, text="New result available!",
                    files=[archive])

    print("End of main function")

if __name__ == "__main__":  # pragma: no cover
    main()