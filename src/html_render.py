from src import data
import datetime
import html as html_mod

HOURS_PER_DAY = [
    "12 AM", "1 AM", "2 AM", "3 AM", "4 AM",
    "5 AM", "6 AM", "7 AM", "8 AM", "9 AM",
    "10 AM", "11 AM", "12 PM", "1 PM", "2 PM", "3 PM", "4 PM",
    "5 PM", "6 PM", "7 PM", "8 PM", "9 PM",
    "10 PM", "11 PM"
]
DAYS_PER_WEEK = ["Mon", "Tue", "Wed", "Thr", "Fri", "Sat", "Sun"]
HOURS_PER_WEEK = []

# Generate the hours per week array
for day in DAYS_PER_WEEK:
    for hour in HOURS_PER_DAY:
        HOURS_PER_WEEK.append(day + " " + hour)


def generate_date_range(start_date, days):
    """
    Returns an array of date strings, in the format
    YYYY-MM-DD

    :param start_date: Start time, datetime object.
    :param days: Days in the range, including start_date
    :return: String array of date objects
    """
    dt = datetime.timedelta(days=1)
    returned = []
    for i in range(days):
        returned.append(start_date.strftime('%Y-%m-%d'))
        start_date += dt
    return returned


""" Some misc array util, basically
calls list() on a function that normally
returns an iterator, such as filter or range,
to save time in typing """


def filter_list(f, l):
    return list(filter(f, l))


def map_list(f, l):
    return list(map(f, l))


def reversed_list(l):
    return list(reversed(l))


def str_list(i):
    return str(list(i))


""" Some misc HTML util; generates repetitive
HTML code snippets """


def generate_trace(prefix, n):
    """
    Returns an array of variable names. For
    example, generate_trace("trace", 2) returns
    ["trace1", "trace2"]

    :param prefix: prefix of the variable name
    :param n: number of variables
    :return: array of named variables
    """
    returned = []
    for i in range(n):
        returned.append(prefix + str(i + 1))
    return returned


def generate_deviation(average, value):
    """
    Given a value and an average, returns a colored
    HTML snippet showing how much above/below the
    average the value is

    :param average: Average value
    :param value: Value to compare
    :return: HTML snippet
    """
    return \
        "&nbsp; <span style='color: green'>(+{:0.2f})</span>".format(value - average) \
        if value >= average else \
        "&nbsp; <span style='color: red'>(-{:0.2f})</span>".format(average - value)


def generate_stacked_bar_graph(x_axis, y_axii, names, id, height=300, height_padding=35):
    """
    Generates the <script> tag to graph a
    stacked vertical bar graph.

    :param x_axis: Array of x axis points
    :param y_axii: Array of array of y axis points
        Each element is an array of the y-axis point of a
        "stack" in the graph
    :param names: String array of names, to label each "stack"
    :param id: id of the graph element
    :param height: height of the graph, default 300 (px)
    :param height_padding: bottom padding of the graph, default 35 (px)
    :return: HTML code
    """

    html = "<script>"
    var_count = 1
    x_axis = str_list(x_axis)

    for i in range(len(y_axii)):
        html += "var trace" + str(var_count) + " = {\n"
        html += "   x: " + x_axis + ",\n"
        html += "   y: " + str(y_axii[i]) + ",\n"
        html += "   name: '" + names[i] + "',\n"
        html += "   type: 'bar'\n"
        html += "};\n"
        var_count += 1

    html += "var data = [" \
            + ", ".join(generate_trace("trace", len(names))) \
            + "];\n"

    html += "Plotly.newPlot('" + id + """', data, {
        barmode: "stack", 
        margin: { l: 25, r: 25, b: """ + str(height_padding) + """, t: 25, pad: 4 },
        plot_bgcolor: "#FCFCFC",
        paper_bgcolor: "#FCFCFC",
        height: """ + str(height) + """
    });\n"""
    html += "</script>"
    return html


""" Renders a conversation into a neat HTML file"""


def render(conversation):
    """
    Renders a conversation object into
    an HTML file (string)

    :param conversation: Conversation object
    :return: HTML String
    """

    data_date_range = generate_date_range(conversation.analysis.first_message_timestamp,
                            conversation.analysis.days_in_range)

    html = """
    <title>Chat Statistics</title>
    <link href="https://fonts.googleapis.com/css?family=Open+Sans:400,700" rel="stylesheet">
    <link rel="stylesheet" href="stats.css">  
    
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>        

    <h1 style="font-weight: 700; font-size: 60px">Chat Statistics</h1><br>
    <span class="light-gray">{} to {} ({:,} days)</span><br>
    <br>
    The most active day was <b>{} ({:,} messages)</b><br>
    Active days account for <b>{:0.2f}%</b> of all days<br><br>
    
    <h2 class="light-gray small-title">Overview</h2><br>
    <table style="width:100%">
        <tr>
            <td class="border-top">
                <small>Persons Involved</small><br>
                <span class="large-bold light-blue-gray">{:,}</span>
            </td>
            <td class="border-top">
                <small>Mum. Active Days</small><br>
                <span class="large-bold light-blue-gray">{:,}</span>
            </td> 
            <td class="border-top">
                <small>Mum. Inactive Days</small><br>
                <span class="large-bold light-blue-gray">{:,}</span>
            </td> 
        </tr>
    </table>

    <h2 class="light-gray small-title">Totals</h2><br>
    <table style="width:100%">
        <tr>
            <td class="border-top">
                <small>Messages</small><br>
                <span class="large-bold light-blue-gray">{:,}</span>
            </td>
            <td class="border-top">
                <small>Words</small><br>
                <span class="large-bold light-blue-gray">{:,}</span>
            </td> 
            <td class="border-top">
                <small>Characters</small><br>
                <span class="large-bold light-blue-gray">{:,}</span>
            </td> 
            <td class="border-top">
                <small>Chars. (no spaces)</small><br>
                <span class="large-bold light-blue-gray">{:,}</span>
            </td> 
        </tr>
    </table>

    <h2 class="light-gray small-title">Averages</h2><br>
    <table style="width:100%">
        <tr>
            <td class="border-top">
                <small>msg / day (active)</small><br>
                <span class="large-bold light-blue-gray">{:0.2f}</span>
            </td>
            <td class="border-top">
                <small>msg / day (all)</small><br>
                <span class="large-bold light-blue-gray">{:0.2f}</span>
            </td> 
            <td class="border-top">
                <small>Words per message</small><br>
                <span class="large-bold light-blue-gray">{:0.2f}</span>
            </td> 
            <td class="border-top">
                <small>Letters per word</small><br>
                <span class="large-bold light-blue-gray">{:0.2f}</span>
            </td> 
        </tr>
    </table>

    <h2 class="light-gray small-title">Content</h2><br>
    <table style="width:100%">
        <tr>
            <td class="border-top">
                <small>Swears</small><br>
                <span class="large-bold light-blue-gray">{:,}</span>
            </td>
            <td class="border-top">
                <small>Questions</small><br>
                <span class="large-bold light-blue-gray">{:,}</span>
            </td> 
            <td class="border-top">
                <small>URLs</small><br>
                <span class="large-bold light-blue-gray">{:,}</span>
            </td> 
        </tr>
    </table>
    <br>
    
    <h2 class="light-gray small-title">Some Urls Posted</h2><br>
    {}<br><br>
    
    <h2 class="light-gray small-title">First Message Sent</h2><br>
    <blockquote>{}
    <span>{}</span>
    </blockquote>
    <br><br>
    
    <h2>Activity Per Person</h2><br>
            """.format(
        conversation.analysis.first_message_timestamp.date(),
        conversation.analysis.last_message_timestamp.date(),
        conversation.analysis.days_in_range,

        conversation.analysis.most_active_day.date(),
        conversation.analysis.most_messages_said,
        conversation.analysis.active_days / conversation.analysis.days_in_range * 100,

        len(conversation.persons.keys()),

        conversation.analysis.active_days,
        conversation.analysis.days_in_range - conversation.analysis.active_days,

        conversation.analysis.total_messages,
        conversation.analysis.total_words,
        conversation.analysis.total_characters,
        conversation.analysis.total_characters_without_spaces,

        conversation.analysis.total_messages / conversation.analysis.active_days,
        conversation.analysis.total_messages / conversation.analysis.days_in_range,
        conversation.analysis.total_words / conversation.analysis.total_messages,
        conversation.analysis.total_characters_without_spaces / conversation.analysis.total_words,

        conversation.analysis.swears,
        conversation.analysis.questions,
        len(conversation.analysis.urls),
        "<br>".join(map_list(
            lambda x: "<a href=\"" + x + "\" class=\"url\">" + x + "</a>",
            conversation.analysis.urls[0: 8])),

        conversation.analysis.first_message.content,
        conversation.name_map.get(conversation.analysis.first_message.username, conversation.analysis.first_message.username),
    )

    highest_user_messages = max(map_list(lambda x: max(x.analysis.active_days_all_time), conversation.persons.values()))

    html += "<table style='width: 100%'>"

    for name, user in conversation.persons.items():
        html += """
    <tr>
        <td style="padding: 10px; width: 200px">
            <h3 class="large-bold light-blue-gray" 
                style="font-size: 24px; width: 200px">""" + name + """</h3>
        </td>
        <td class='user_graph_1' id='""" + name + """'></td>
    </tr>
    <script>
    var trace = {
        x: """ + str(data_date_range) + """,
        y: """ + str(user.messages_all_time) + """,
        type: 'bar',
        marker: {  color: '#455A64' }
    };

    var data = [trace];

    var layout = {
        showlegend: false,
        height: 120,
        width: 800,
        plot_bgcolor: "#FCFCFC",
        paper_bgcolor: "#FCFCFC",
        margin: { l: 25, r: 25, b: 35, t: 25, pad: 4 },
        yaxis: {
            zeroline: false,
            gridwidth: 2,
            range: [0, """ + str(highest_user_messages) + """]
        },
        bargap: 0.0,
    };

    Plotly.newPlot(""" + name + """, data, layout);
    </script>"""

    html += "</table>"

    # ----------------------------------------------
    # Activity percentages
    #
    # Pie chart of the number of messages per user
    # divided by total messages
    # ----------------------------------------------
    html += "<br><br><h2>Percentage Share of Activity Per Person</h2><br>"
    html += "<table style='width: 100%'><tr><td style='width: 300px'>"
    html += "<table>"

    for name, user in conversation.persons.items():
        html += "<tr><td class='small-td'><b>"
        html += name + "</b></td><td class='small-td'>" \
                     + "{:0.2f}%<br>".format(user.analysis.total_messages
                     / conversation.analysis.total_messages * 100)
        html += "</td></tr>"
    html += "</table></td><td>"

    html += """
    <div id="user_activity_pie_chart"></div>
    <script>
        var data = [{
            values: """ + str(
        map_list(lambda x: x.analysis.total_messages / conversation.analysis.total_messages, conversation.persons.values())) + """,
            labels: """ + str(list(conversation.persons.keys())) + """,
            type: 'pie'
        }];

        Plotly.newPlot("user_activity_pie_chart", data, {
            height: 300,
            width: 500,
            margin: { l: 25, r: 25, b: 35, t: 25, pad: 4 },
            plot_bgcolor: "#FCFCFC",
            paper_bgcolor: "#FCFCFC",
        });
    </script>"""

    html += "</td></tr></table>"

    # ----------------------------------------------
    # Activity over the entire period
    #
    # A graph of the number of messages per day, with the number of
    # messages from each user stacked on top of each other, over
    # the entire duration of analysis
    # ----------------------------------------------
    html += """
    <br>
    <h2>Activity Over Entire Period</h2><br>
    <div id="stacked_activity_all"></div>\n"""

    y_axii = []
    names = []
    for name, user in conversation.persons.items():
        y_axii.append(user.messages_all_time)
        names.append(name)

    html += generate_stacked_bar_graph(
        data_date_range,
        y_axii, names, "stacked_activity_all", 350, 55)

    # ----------------------------------------------
    # Activity per day of the week
    #
    # A graph of the number of messages per day, with the number of
    # messages from each user stacked on top of each other, over
    # each day of the week
    # ----------------------------------------------
    html += """
    <br>
    <h2>Activity Per Day of Week &nbsp; &nbsp; (STACK, TOP) (SIDE, BOTTOM)</h2><br>
    <div id="activity_per_day_week_stacked"></div>\n"""

    y_axii = []
    for name, user in conversation.persons.items():
        y_axii.append(user.analysis.active_days_of_week)

    html += generate_stacked_bar_graph(
        DAYS_PER_WEEK,
        y_axii, names, "activity_per_day_week_stacked", 220)

    html += """
    <div id="activity_per_week_day_side"></div>
    <script>
        Plotly.newPlot("activity_per_week_day_side", data, {
            barmode: "group",
            margin: { l: 25, r: 25, b: 35, t: 25, pad: 4 },
            plot_bgcolor: "#FCFCFC",
            paper_bgcolor: "#FCFCFC",
            height: 220
        });
    </script>"""

    # ----------------------------------------------
    # Most active hour of the day
    #
    # A graph of the activity per hour of the entire period
    # stacked per person.
    # ----------------------------------------------
    html += """
    <br>
    <h2>Most Active Hour of Day</h2><br>
    <div id="most_active_hour_day"></div>
    <script>

    """
    i = 0
    for name, user in conversation.persons.items():
        html += """
            var trace""" + str(i) + """ = {
                x: """ + str(HOURS_PER_DAY) + """,
                y: """ + str(user.analysis.active_hours) + """,
                name: '""" + name + """',
                type: 'bar'
            }; """
        i += 1
    html += """
    var data = """ + str(
        list(map(lambda x: "trace" + str(x), list(range(len(conversation.persons.items())))))).replace("'", "") + """;
    var layout = {
        barmode: "stack",
        margin: { l: 25, r: 25, b: 35, t: 25, pad: 4 },
        plot_bgcolor: "#FCFCFC",
        paper_bgcolor: "#FCFCFC",
        height: 220
    };
    Plotly.newPlot("most_active_hour_day", data, layout);
    </script> """

    # ----------------------------------------------
    # Activity per hour of the week
    #
    # A graph of the number of messages per hour, over
    # every hour in the entire week, with user counts
    # stacked on top of each other
    # ----------------------------------------------
    html += """
        <br>
        <h2>Most Active Hour of the Week</h2><br>
        <div id="most_active_hour_week"></div>
        <script>\n"""

    i = 1
    days_range = str(HOURS_PER_WEEK)

    for name, user in conversation.persons.items():
        html += "var trace" + str(i) + " = {\n"
        html += "   x: " + days_range + ",\n"
        html += "   y: " + str(user.analysis.active_weekly_hours) + ",\n"
        html += "   name: '" + name + "',\n"
        html += "   type: 'bar'\n"
        html += "};\n"
        i += 1
    html += "var data = [" \
            + ", ".join(generate_trace("trace", len(conversation.persons.items()))) \
            + "];\n"
    html += """
        Plotly.newPlot("most_active_hour_week", data, {
            barmode: "stack",
            margin: { l: 25, r: 25, b: 75, t: 25, pad: 4 },
            plot_bgcolor: "#FCFCFC",
            paper_bgcolor: "#FCFCFC",
            height: 260
        });
        </script> """

    # ----------------------------------------------
    # Most common words used
    #
    # Shows most common words and their usage count, not
    # including english stopwords
    # ----------------------------------------------
    stopwords_removed = filter_list(lambda x: x[0].lower() not in data.STOPWORDS,
                                    conversation.analysis.word_freq_sorted)

    html += """
    <br>
    <h2>Commonly used words</h2><br>
    <div id="common_words"></div>
    <small>*Excluding common english stopwords</small>
    
    <script>
    var data = [{
        type: 'bar',
        x: """ + str(reversed_list(map_list(lambda x: x[1], stopwords_removed[0:15]))) + """,
        y: """ + str(reversed_list(map_list(lambda x: x[0], stopwords_removed[0:15]))) + """,
        orientation: 'h'
    }];
    
    Plotly.newPlot("common_words", data, {
        margin: { l: 50, r: 25, b: 35, t: 25, pad: 4 },
        plot_bgcolor: "#FCFCFC",
        paper_bgcolor: "#FCFCFC",
        height: 300
    });
    </script> """

    # ----------------------------------------------
    # Per Person Statistics
    # ----------------------------------------------
    html += "<br><br><h2>Per Person Statistics</h2>"
    for name, user in conversation.persons.items():
        html += "<br><br><h2 style='font-size: 24px' class='large-bold light-blue-gray'>" + name + "</h2><br>"
        html += "<b>Common Words:</b> "

        stopwords_removed = filter_list(
                                 lambda x: x[0].lower() not in data.STOPWORDS and len(x[0]) >= 3,
                                 user.analysis.word_freq_sorted)[0:30]
        for word in stopwords_removed:
            html += word[0] + " <span style='color: gray'>(" + str(word[1]) + ")</span> "

        html += "<br><br>"
        html += "<table class='simple-table float-left'>"
        html += "<tr><td>Total Messages</td><td>{:,}</td>".format(user.analysis.total_messages)
        html += "<tr><td>Total Words</td><td>{:,}</td>".format(user.analysis.total_words)
        html += "<tr><td>Active Days</td><td>{:,}</td>".format(user.analysis.active_days)
        html += "</table>"

        html += "<table class='simple-table float-left'>"
        html += "<tr><td>Words Per Message</td><td>{:0.2f} {}</td>"\
            .format(user.analysis.total_words / user.analysis.total_messages,
                    generate_deviation(
                        conversation.analysis.total_words / conversation.analysis.total_messages,
                        user.analysis.total_words / user.analysis.total_messages
                    ))
        html += "<tr><td>Chars Per Message</td><td>{:0.2f} {}</td>"\
            .format(user.analysis.total_characters / user.analysis.total_messages,
                    generate_deviation(
                        conversation.analysis.total_characters / conversation.analysis.total_messages,
                        user.analysis.total_characters / user.analysis.total_messages
                    ))
        html += "<tr><td>Letters per word</td><td>{:0.2f} {}</td>"\
            .format(user.analysis.total_characters_without_spaces / user.analysis.total_words,
                    generate_deviation(
                        conversation.analysis.total_characters_without_spaces / conversation.analysis.total_words,
                        user.analysis.total_characters_without_spaces / user.analysis.total_words
                    ))
        html += "</table>"

        html += "<table class='simple-table float-left'>"
        html += "<tr><td>Swears</td><td>{:,}</td>".format(user.analysis.swears)
        html += "<tr><td>Questions</td><td>{:,}</td>".format(user.analysis.questions)
        html += "<tr><td>URLs</td><td>{:,}</td>".format(len(user.analysis.urls))
        html += "</table>"

        html += "<br><br><br><br>"
        html += "<blockquote>{}<span>First Message Sent</span></blockquote>".format(html_mod.escape(user.analysis.first_message.content))
        html += "<blockquote>{}<span>Random Quote</span></blockquote>".format(html_mod.escape(user.random_quote))

        html += "<br><b>Common Responses:</b><br>"

        common_responses = list(set(user.common_responses))[0: 15]
        html += "<div>{}</div>".format(
            " ".join(map_list(lambda x: "<div class='badge'>" + html_mod.escape(x) + "</div>", common_responses)))

        html += "<br><br>"
    return html
