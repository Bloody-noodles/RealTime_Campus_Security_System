from datetime import datetime

EVENTS = []

MAX_EVENTS = 50


class Timeline:

    def add(self, icon, title, description):

        EVENTS.insert(

            0,

            {

                "time": datetime.now().strftime("%H:%M:%S"),

                "icon": icon,

                "title": title,

                "description": description

            }

        )

        del EVENTS[MAX_EVENTS:]

    def all(self):

        return EVENTS