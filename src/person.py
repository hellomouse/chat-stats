"""
Person class, see help for Person
for more information.
"""

from src import analyser
from src import data
import random


class Person(object):
    """
    Person

    A person class, which represents a user
    in the chat. Contains a list of their
    messages, and extra statistics.
    """

    def __init__(self, name, messages):
        """
        Create a person object.

        :param name: Name of the person
        :param messages: Array of Message objects the person said
            Must be sorted from earliest to latest
        """

        self.name = name
        self.messages = messages
        self.messages_all_time = []

        if len(messages) > 0:
            self.analysis = analyser.BasicAnalyser(messages)
            self.random_quote = random.choice(messages).content

            self.common_responses = []
            self.get_common_responses()

    def recompute(self):
        """
        Recalculates all instance variables in case messages
        were updated after construction. Assumes self.messages
        has a length > 0
        """

        self.analysis = analyser.BasicAnalyser(self.messages)

        # Attempt to select a meaningful quote (> 5 words in
        # length). Because the user might have never said
        # a meaningful quote, we will only try 15 times
        for i in range(15):
            self.random_quote = random.choice(self.messages).content
            if len(self.random_quote.split(" ")) > 5:
                break

        self.common_responses = []
        self.get_common_responses()

    def compute_messages_all_time(self, days_in_range, start_date):
        """
        Calculates the messages_all_time array

        :param days_in_range: Days in the entire conversation
        :param start_date: Start date of entire conversation
        :return: None
        """

        self.messages_all_time = [0] * days_in_range

        # Calculate all time messages/day statistics
        messages_said = 0
        current_timestamp = self.analysis.first_message_timestamp

        for message in self.messages:
            if current_timestamp is None or message.timestamp.date() != current_timestamp.date():
                self.messages_all_time[(message.timestamp - start_date).days] = messages_said
                current_timestamp = message.timestamp
                messages_said = 0

            messages_said += 1

    def get_common_responses(self):
        """
        A response is a short message (<5 words) that contains
        phrases like "lol", "thanks", "good job", etc...

        This returns a list of responses the user has said
        """
        for message in self.messages:
            if any(" " + d + " " in " " + message.content.lower() + " " for d in data.RESPONSES) \
                    and len(message.content.split(" ")) < 5:
                self.common_responses.append(message.content)

    def __str__(self):
        """
        Convert person to a string
        :return: The name of the person
        """
        return self.name

    def to_dict(self):
        """
        Returns a dictionary representation of the object
        :return: dict representation
        """
        return {
            "analysis": self.analysis.to_dict(),
            "messages": list(map(lambda x: str(x), self.messages)),
            "messages_all_time": self.messages_all_time,
            "common_responses": self.common_responses,
            "random_quote": self.random_quote
        }
