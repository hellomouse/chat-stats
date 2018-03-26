"""
Conversation and Message class
is contained in this file
"""

import glob
import datetime
import json
import html

from src import person
from src import analyser
from src import html_render


class Message(object):
    """
    Holds a Message sent by a user.
    """

    def __init__(self, username, content, timestamp, raw):
        """
        Create a new Message object

        :param username: Username of the person who said the message
        :param content: Content of the message
        :param timestamp: Timestamp of the message (In yyyy-mm-ddThh:mm:ss format)
        :param raw: Raw match, in case you need to use it
        """
        self.username = username
        self.content = content
        self.raw = raw
        self.timestamp = datetime.datetime.strptime(timestamp.split(".")[0], "%Y-%m-%dT%H:%M:%S")

    def __str__(self):
        return "{} {}: {}".format(self.timestamp, self.username, self.content)


class Conversation(object):
    """
    Conversation object, contains the
    entire chat
    """

    def __init__(self, path, extract,
                 extract_messages=lambda x: x.split("\n"),
                 sort_files=lambda x: sorted(x),
                 name_map={}):
        """
        Create a Conversation Object

        :param path: path to the files containing the chat logs
            Use a wildcard (*) to match all files
        :param extract: A function that given a line, returns either
            An array in this format: [username, content, timestamp in
                "yyyy-mm-ddThh:mm:ss" format, raw_content]
            or False, if the line is not a valid message
        :param extract_messages: A function that given the raw text
            content of a file, returns a String array of each message, 1 per line
        :param sort_files: A function that given a String array of file names,
            sorts them in sequential order
        :param name_map: Optional name map - maps the name that
            appears in the chatlog to something else. For example,
            if the chatlog contains phone numbers, a name_map could
            be

            {
                "+11234567890": "John Smith"
            }

            which would replace the phone number with the name
            in processing
        """

        self.path = path
        self.files = glob.glob(path)
        self.messages = []

        self.extract = extract
        self.extract_messages = extract_messages
        self.sort_files_raw = sort_files

        self.sort_files()
        self.load_messages()
        self.messages.sort(key=lambda x: x.timestamp)
        self.analysis = analyser.BasicAnalyser(self.messages)

        self.name_map = name_map
        self.persons = {}

        for message in self.messages:
            username = html.escape(self.name_map.get(message.username, message.username))
            self.persons[username] = self.persons.get(username) or person.Person(username, [])
            self.persons[username].messages.append(message)

        for key, value in self.persons.items():
            value.recompute()
            value.compute_messages_all_time(self.analysis.days_in_range, self.analysis.first_message_timestamp)

    def sort_files(self):
        """Sort the classes' file array by filename. Examples of
           how the file names are sorted:

           "file-2017" comes before "file-2018"
           "file-2017" comes after "file-2017(1)"
           "file-2017(1)" comes after "file-2017(2)

            Precondition: File names must end either in " - {4 digit year}"
            or " - {4 digit year}({number})"
        """
        self.files = self.sort_files_raw(self.files)

    def load_messages(self):
        """Load all the conversations from self.files, and
           add the new Message objects to self.messages"""
        for f in self.files:
            f_obj = open(f, "r", encoding="utf8")
            self.extract_messages_from_text(f_obj.read())
            f_obj.close()

    def extract_messages_from_text(self, data):
        """Given some text, extracts the messages from the data
           and adds the new Message objects to self.messages"""
        messages = self.extract_messages(data)

        for message in messages:
            data = self.extract(message)
            if not data:
                continue
            self.messages.append(Message(data[0], data[1], data[2], data[3]))

    def generate_html(self):
        """Returns an HTML string representing the statistics
        for the conversation"""
        return html_render.render(self)

    def generate_json(self):
        """Returns a JSON representation of the conversation"""
        return json.dumps({
            "messages": list(map(lambda x: str(x), self.messages)),
            "analysis": self.analysis.to_dict(),
            "users": {k: v.to_dict() for k, v in self.persons.items()}
        }, sort_keys=True, indent=4, separators=(',', ': '))

    def generate_output(self):
        """Updates the output folder"""
        f = open("output/stats.html", "w", encoding="utf-8")
        f.write(self.generate_html())
        f.close()

        f = open("output/stats.json", "w", encoding="utf-8")
        f.write(self.generate_json())
        f.close()
