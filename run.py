"""
Telegram Event Name Updater
Copyright (C) 2024-2025 Julian Metzler

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import asyncio
import datetime
import requests

from dateutil import parser
from ics import Calendar
from pyrogram import Client
from pyrogram.raw import functions

from secrets import API_ID, API_HASH, ICAL_URL
from settings import EVENT_LOOKAHEAD_DAYS


def get_event_short_name(event):
    if event.description is None:
        return None
    desc_lines = event.description.splitlines()
    for line in desc_lines:
        if line.startswith("tg-name:"):
            name = line.lstrip("tg-name:").strip()
            return name
    return None

def generate_event_tags():
    current = []
    future = []
    now = datetime.datetime.now().astimezone()
    
    cal = Calendar(requests.get(ICAL_URL).text)
    events = list(cal.timeline)
    
    for event in events:
        delta = event.begin - now
        # Add current event(s)
        if (event.begin <= now <= event.end):
            name = get_event_short_name(event)
            if name:
                current.append(name)
        # Skip events in the past
        elif (now >= event.end):
            continue
        # Skip events too far in the future
        elif (delta.days > EVENT_LOOKAHEAD_DAYS):
            continue
        # Add future event(s)
        else:
            name = get_event_short_name(event)
            if name:
                future.append(name)
    
    name = ""
    if current:
        name += "@ " + ", ".join(current)
    if future:
        if current:
            name += " "
        name += "→ " + ", ".join(future)
    return name

async def update_name(event_tags):
    app = Client("event_name_update", api_id=API_ID, api_hash=API_HASH)
    async with app:
        await app.invoke(functions.account.UpdateProfile(last_name=event_tags))


def main():
    name = generate_event_tags()
    print("Updating last name:", name)
    asyncio.run(update_name(name))


if __name__ == "__main__":
    main()
