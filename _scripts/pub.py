import requests
import sys
from lxml import html
from collections import namedtuple


Paper = namedtuple('Paper', ['key', 'url', 'authors', 'title', 'partof'])


def download_record(record_url):
    """Returns a Paper object for a given key"""
    text = requests.get(record_url).text
    tree = html.fromstring(text)
    entry = next(iter(tree.cssselect('li.entry')))
    key = entry.get('id')
    url = entry.cssselect('a[itemprop=url]')[0].get('href')
    authors = [x.text_content()
               for x in entry.cssselect('span[itemprop=author]')]
    title = entry.cssselect('span.title')[0].text_content().rstrip('.')
    details = entry.xpath('(.//a)[last()]')
    details += entry.xpath('(.//a)[last()]/following-sibling::*')
    partof = [x.text_content() + (x.tail if x.tail else '')
              for x in details]
    return Paper(key, url, authors, title, partof)


if __name__ == '__main__':
    paper = download_record(sys.argv[1])
    print('  <li>', ', '.join(paper.authors), ':<br>', sep='')
    print('    <a href="', paper.url, '">', sep='')
    print('      ', paper.title, '</a>', sep='')
    print('<br>')
    print('    ', *paper.partof, sep='')
    print('  </li>')
