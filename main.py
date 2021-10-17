import nodeextractor as extractor
import nodesearch as search
import webbrowser
import os
import io


max_node_count = 124229
test_node = 'https://forums.spiralknights.com/en/node/123879'


def get_node_url(node):
    return f'https://forums.spiralknights.com/en/node/{node}'


def get_all_forum_nodes():
    i = 0
    while i < max_node_count:
        # Get the next url
        url = get_node_url(i)
        print(url)

        # Create/Open a text file to write to
        file = open(f'output/forums.txt', "w+")
        x = extractor.extract_content(url)
        file.write(x)
        file.close()

        # Increment node
        i += 1
        print(f'{i} / {max_node_count}')


def get_forum_node(node):
    url = get_node_url(node)
    content = extractor.extract_content(url)
    return content


node_url_page = 'https://forums.spiralknights.com/en/node/'
bazaar_page_url = 'https://forums.spiralknights.com/en/forum/41?page='
bazaar_pages = 1841


def get_bazaar_nodes():
    i = 1291
    while i < bazaar_pages:
        page = f'{bazaar_page_url}{i}'
        print(page)
        nodes = get_nodes_on_page(page)
        print('Extracting data from bazaar nodes')
        for n in nodes:
            # print(n)
            with io.open(f'output/bazaar.txt', "a+", encoding="utf-8") as f:
                node_url = f'<a href={node_url_page}{n}>{node_url_page}{n}</a>'
                f.write(node_url)
                f.write(get_forum_node(n))
                f.close()
        print(f'Successfully extracted data from page{i}')
        i += 1


def get_nodes_on_page(page):
    nodes = extractor.extract_nodes_from_page(page)
    print(nodes)
    return nodes


def search_item(item):
    lines = search.filter_item(item, contain_all=False)
    new = 2

    path = f'output/{item}.html'
    with open(path, "a+", encoding='utf-8') as f:
        f.write(lines)
        f.close()
    webbrowser.open('file://' + os.path.realpath(path), new=new)


print('Separate words or groups of words by commas to search for multiple items at the same time.')
print('Example: caladbolg, overcharged mixmaster, legobuild')
print('')
print('Just like ctrl+f it searches for the exact word.')
print('Since people use many different terms for mixmaster. It may be beneficial to search for multiple terms.')
print('Example: mixer, mixmaster, mixermaster')
print('')
print("Capitals don't matter.")
print('')
print('The results are saved in the output folder.')
while True:
    search_item(input('Input an item to search '))

