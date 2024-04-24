"""
Telegram Event Name Updater
Copyright (C) 2024 Julian Metzler

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
import csv
import datetime

from dateutil import parser
from pyrogram import Client
from pyrogram.raw import functions

from secrets import API_ID, API_HASH
from settings import EVENT_LOOKAHEAD_DAYS


def generate_event_tags():
    current = []
    future = []
    now = datetime.datetime.now().astimezone()
    with open("events.csv", 'r') as f:
        reader = csv.DictReader(f)
        for event in reader:
            start_dt = parser.parse(event['start'])
            end_dt = parser.parse(event['end'])
            delta = start_dt - now
            # Add current event(s)
            if (start_dt <= now <= end_dt):
                current.append(event['name'])
            # Skip events in the past
            elif (now >= end_dt):
                continue
            # Skip events too far in the future
            elif (delta.days > EVENT_LOOKAHEAD_DAYS):
                continue
            # Add future event(s)
            else:
                future.append(event['name'])
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
