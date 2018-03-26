import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import src as stats


def extract(line):
    # Ignore any lines that start with --
    # in this example
    if line.startswith("--"):
        return False

    # Timestamp should be in
    # yyyy-mm-ddThh:mm:ss format
    timestamp = line.split(" ")[0]

    # Extract username
    username = line.split("<")[1].split(">")[0]

    # Message content
    content = line.split("> ")[1]

    # (Last item in output is raw data - used only
    #  for debugging)
    return [username, content, timestamp, line]


def extract_messages(text):
    # Because there is 1 message per line
    # we can split the file on a newline
    # to get each message. Your log file
    # may vary
    return text.split("\n")


def sort_files(file_names):
    # Sort the file names. If you have a conversation
    # split over multiple files, you can write your
    # own sort function to sort the files into sequential
    # order
    return sorted(file_names)


# If someone wants to be displayed as an alias,
# use <name in logs> : <alias> to modify what
# their name is displayed as. Useful for user ids.
#
# For example, if I was represented as "id:12345" in
# the logs, I could renamed myself by doing
# name_map = { "id:12345" : "My real username" }
name_map = {
    "Bob": "Bobby"
}

print("Starting analysis...")
c = stats.conversation.Conversation("example/sample_conversation.txt",
                                    extract,
                                    extract_messages,
                                    sort_files,
                                    name_map)
c.generate_output()
print("Done generating output!")
