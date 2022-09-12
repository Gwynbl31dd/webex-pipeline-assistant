"""
pipeline_assistant base module.

This is the principal module of the pipeline_assistant project.
here you put your main classes and objects.

Be creative! do whatever you want!
"""

class Webex_helper:
    """
    This is the main class of the Cisco_project project.
    Use this as an example to create your own class.
    Use the snippets to help your building the functionality (ctrl+space)
    """
    # Constructor
    def __init__(self,api):
        self.api = api

    def create_rooms(self, rooms):
        available_rooms = []
        for room in rooms:
            room_exist = False
            for existing_room in self.api.rooms.list():
                if room == existing_room.title:
                    print(f'Room {room} already exists')
                    available_rooms.append(existing_room)
                    room_exist = True
                    break
            if not room_exist:
                print(f'Room {room} does not exist')
                available_rooms.append(self.api.rooms.create(room))

        return available_rooms

    def subscribe_people(self,people,available_rooms):

        for person in people:
            print(f'Person {person}')
            for profile in self.api.people.list(email=person):
                print(f'subscribe {profile.displayName}')
                # Add the person to the rooms
                for room in available_rooms:
                    is_member = False
                    for _ in  self.api.memberships.list(roomId=room.id, personId=profile.id):
                        is_member = True 
                    if not is_member:
                        self.api.memberships.create(room.id, personId=profile.id, isModerator=False)