# Telegram Event Name Updater

## What does this do?
This little tool updates your Telegram last name based on an iCal URL with events that you plan on attending.
You can configure a cutoff, i.e. how many days events may be in the future at most to be included. The default setting is 6 months.

The tool will format your last name like this:
* If you're attending EVENT1 right now and EVENT2 and EVENT3 are in the future: `@ EVENT1 → EVENT2, EVENT3`
* If you're attending EVENT1 right now and no other events are in the future: `@ EVENT1`
* If you're not attending any event right now and EVENT1 and EVENT2 are in the future: `→ EVENT1, EVENT2`
* If you're attending EVENT1 and EVENT2 right now (how?) and EVENT3 is in the future: `@ EVENT1, EVENT2 → EVENT3`
* If you're not attending any event and no event is in the future, the last name will be blank.

## What do I need?
You will need a Telegram API ID and API Hash (this is different from a Telegram Bot), which you can get [here](https://core.telegram.org/api/obtaining_api_id).

On first run, the script will ask you for your Telegram phone number to log in.

You need to rename `secrets.example.py` to `secrets.py` and add your API ID and API Hash before running the script.

You should set up the script to run regularly, ideally once per hour, via a cronjob.

## How do I add events?
The script will check all events in the specified iCal calendar for the special tag "tg-name" in the event's description.
So if you want to include an event in your Telegram name, just add one line to the event description as follows: `tg-name: ABC`.
This will cause the event to show up as "ABC" in your Telegram name, no matter what the event is actually called.