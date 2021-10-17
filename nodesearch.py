import io
import textwrap

node = "https://forums.spiralknights.com/en/node/"
node_start = "<a href="
node_end = "</a>"
node_link_end = ">"
years = ['2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021']


def filter_item(search, contain_all=False):
    # Using commas will search for each item individually
    search = search.split(',')
    search = list(map(str.strip, search))

    print(f'Searching for the following: {search}')
    last_author = ""
    last_node = ""
    lines = "<strong>Format is mm/dd/yyyy, timezone is in EST.</strong><br>"
    with io.open(f'bazaar.txt', "r", encoding="utf-8") as bazaar:
        for line in bazaar:
            if is_date(line):
                last_author = line
            if node in line:
                # Find where the node link starts and ends
                index = line.find(node)
                end_index = line.find(node_link_end)

                # Get the node
                n = line[index:end_index]

                # Create the node link
                link = node_start + n + node_link_end + n + node_end

                # Un indent the link and test if the lines are equal
                new_line = textwrap.dedent(line)

                # If the lines are equal this is a node link and not a link in a different forum
                if link in new_line:
                    last_node = line
            if contain_all is False:
                if any(item.lower() in line.lower() for item in search):
                    lines += f'{last_node}{line}<strong>by {last_author}</strong><br>'
            else:
                if all(item.lower() in line.lower() for item in search):
                    lines += f'{last_node}{line}{last_author}<br>'

    return lines


def is_date(line):
    if any(date in line for date in years):
        if line.lower().find('update') == -1:
            if line.lower().find(':') != -1:
                return True
    return False
