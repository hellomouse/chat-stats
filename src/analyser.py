"""
BasicAnalyser class
See BasicAnalayser help for
more information.
"""

import re
from src import data


class BasicAnalyser(object):
    """
    BasicAnalyser

    Only does the basic analysis, ie word count, etc...
    Statistics produced by this class are shared by
    the global chat and individual users
    """

    def __init__(self, messages):
        """
        Construct a BasicAnalyser, which generates some simple
        statistics based on an array of messages.

        :param messages: Array of Message objects to analyse. It is
            required that this parameter have a length > 0
        """

        # Time range of the sample
        self.first_message_timestamp = messages[0].timestamp
        self.last_message_timestamp = messages[-1].timestamp
        self.days_in_range = (self.last_message_timestamp - self.first_message_timestamp).days + 1
        self.active_days = 1

        # Message statistics
        self.total_messages = len(messages)
        self.first_message = messages[0]
        self.last_message = messages[-1]

        self.total_words = 0
        self.total_characters = 0
        self.total_characters_without_spaces = 0

        # Time statistics
        self.active_hours = [0] * 24
        self.active_days_of_week = [0] * 7
        self.active_weekly_hours = [0] * (7 * 24)
        self.active_days_all_time = [0] * self.days_in_range

        # Word statistics
        self.word_count = {}
        self.swears = 0
        self.questions = 0
        self.urls = []

        # Loop through all messages once
        # Updating any needed variables on the way
        self.most_active_day = self.first_message_timestamp
        self.most_messages_said = 0
        self.messages_said_all_time = []

        messages_said = 0
        current_timestamp = self.first_message_timestamp

        for message in messages:
            self.total_words += len(message.content.split(" "))
            self.total_characters += len(message.content)
            self.total_characters_without_spaces += len(message.content.replace(" ", ""))

            if current_timestamp is None or message.timestamp.date() != current_timestamp.date():
                number_missing_days = (message.timestamp - current_timestamp).days
                for i in range(number_missing_days - 1):
                    self.messages_said_all_time.append(0)
                self.messages_said_all_time.append(messages_said)

                current_timestamp = message.timestamp
                self.active_days += 1

                if self.most_messages_said < messages_said:
                    self.most_active_day = current_timestamp
                    self.most_messages_said = messages_said
                messages_said = 0

            messages_said += 1

            self.active_days_all_time[(message.timestamp - self.first_message_timestamp).days] += 1
            self.active_hours[message.timestamp.hour] += 1
            self.active_days_of_week[message.timestamp.weekday()] += 1
            self.active_weekly_hours[message.timestamp.weekday() * 24 + message.timestamp.hour] += 1

            if "?" in message.content:
                self.questions += 1
            if any(" " + swear + " " in " " + message.content + " " for swear in data.SWEARS):
                self.swears += 1

            urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message.content)
            if len(urls) > 0:
                self.urls += urls

            # Count word types
            words = message.content.split(" ")
            for word in words:
                word = word.lower()

                if "http://" in word or "https://" in word:
                    continue
                word = re.sub("[^a-zA-Z]+", "", word)
                if len(word) == 0:
                    continue

                self.word_count[word] = self.word_count.get(word, 0) + 1

        # Word counts
        self.word_freq_sorted = sorted(self.word_count.items(), key=lambda x: x[1], reverse=True)

    def to_dict(self):
        """
        Returns a dict representation of the object
        :return: dict representation
        """
        return {
            "first_message_timestamp": str(self.first_message_timestamp),
            "last_message_timestamp": str(self.last_message_timestamp),
            "days_in_range": self.days_in_range,
            "active_days": self.active_days,
            "total_messages": self.total_messages,
            "total_words": self.total_words,
            "total_characters": self.total_characters,
            "total_characters_without_spaces": self.total_characters_without_spaces,
            "active_hours": self.active_hours,
            "active_days_of_week": self.active_days_of_week,
            "active_weekly_hours": self.active_weekly_hours,
            "active_days_all_time": self.active_days_all_time,
            "word_freq": self.word_freq_sorted,
            "swears": self.swears,
            "questions": self.questions,
            "urls": self.urls,
            "most_active_day": str(self.most_active_day),
            "most_messages_said": self.most_messages_said,
            "messages_said_all_time": self.messages_said_all_time
        }
