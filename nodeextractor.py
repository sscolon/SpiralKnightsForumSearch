import requests
import io


author = '<div class="author-pane-line author-name">'
container_end = '</div>'
tag_end = '>'
content_start = '<div class="content">'
date = '<div class="posted-on">'


def extract_container(content, start_index, search_tag):
    container_start_index = content.find(search_tag, start_index)
    # print(author_container_start_index)
    container_end_index = content.find(tag_end, container_start_index)
    end_index = content.find(container_end, container_end_index)
    result = content[container_end_index+2:end_index]
    # print(result)
    return [result, end_index]


def extract_content(node):
    node_content = requests.get(node).text
    # print(node_content)
    post = ""
    start = 0
    while node_content.find(author, start) != -1:
        # Extract post date
        post_date_data = extract_container(node_content, start, date)
        post_date = post_date_data[0]
        start = post_date_data[1]

        # Extract post author
        post_author_data = extract_container(node_content, start, author)
        post_author = post_author_data[0]
        start = post_author_data[1]

        # Extract post content
        post_content_data = extract_container(node_content, start, content_start)
        post_content = post_content_data[0]
        start = post_content_data[1]

        post += f'\n <strong>{post_author} on {post_date}</strong> \n {post_content}'

    # print(post_content)
    return post


title_start = '<td class="title">'
node_start = '<a href="/en/node/'
node_end = '</a>'
last_node_end_index = 0


def extract_nodes_from_page(page):
    page_content = requests.get(page).text
    nodes = []
    start = 0
    while page_content.find(title_start, start) != -1:
        # Find the start of the node title
        title_start_index = page_content.find(title_start, start)

        # Find the start of the node
        container_start_index = page_content.find(node_start, title_start_index)

        # Find the end of the node
        container_end_index = page_content.find(tag_end, container_start_index)
        result = page_content[container_start_index + 2:container_end_index]

        # Filter out only the node number
        result = result.replace('href="/en/node/', '')
        result = result.replace('"', '')
        result = result.replace(' ', '')
        nodes.append(result)
        start = container_end_index
    return nodes

