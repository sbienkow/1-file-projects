"""Scrape images form pixabay.com ."""
import os
from urllib.request import urlopen, urlretrieve
from urllib.error import URLError
from bs4 import BeautifulSoup as BS
import argparse
from time import sleep


def main():
    args = parser()
    orient = '' if args.o == 'any' else args.o
    name = str(args.n).replace(' ', '+')
    url = ("https://pixabay.com/en/photos/?"
            "q={}&"
            "orientation={}&"
            "min_width={}&"
            "min_height={}")\
            .format(name, orient, args.w, args.h)
    try:
        content = urlopen(url)
    except URLError as err:
        print(err)
    else:
        soup = BS(content.read(), "lxml")
        content.close()
        dir(os.getcwd()+'/images')  # Change directory
        pages = int(soup.find('input', {'name': 'pagi'}).parent.contents[-1]
                    .replace('/', ' ').strip())
        if args.p <= 0:
            print(pages)
        else:
            ran = args.p if args.p <= pages else pages
            print(ran)
            images_left = args.c
            for i in range(1, ran):
                print('Downloading from page {}'.format(i))
                content = urlopen(url+'&pagi={}'.format(i))
                soup = BS(content.read(), "lxml")
                content.close()
                photo_grid = soup.find('div', {'id': 'photo_grid'})
                images = photo_grid.findAll('div', {'class': 'item'})
                for image in images:
                    if image.img.has_attr('srcset'):
                        link = image.img['srcset'].split(' ')[0]
                    elif image.img.has_attr('data-lazy-srcset'):
                        link = image.img['data-lazy-srcset'].split(' ')[0]
                    else:
                        print('Unable to find image link')
                        continue
                    name = link.split('/')[-1]
                    print('N: {}\tL: {}'.format(name, link))
                    urlretrieve(link, name)
                    images_left -= 1
                    if images_left == 0:
                        break
                    sleep(1)  # According to robots.txt Crawl-delay: 1
                if images_left == 0:
                    break
            print("DONE")


def parser():
    """Take care of parsing arguments from CLI."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--n', type=str, default='',
                        help='Name of searched image')
    parser.add_argument('--o', type=str, default='any',
                        choices=['any', 'vertical', 'horizontal'],
                        help='Orientation of image')
    parser.add_argument('--w', type=int, default=0,
                        help='Minimum width in px')
    parser.add_argument('--h', type=int, default=0,
                        help='Minimum height in px')
    parser.add_argument('--p', type=int, default=1,
                        help='Number of pages to download from.'
                        ' If <=0 displays number of pages for current query')
    parser.add_argument('--c', type=int, default=0,
                        help='Limit number of images to download.'
                        ' If non-zero, overrides --p.')
    return parser.parse_args()


def dir(directory):
    """Create directory if it doesn't exist, change directory if it's empty."""
    if not os.path.exists(directory):
        os.makedirs(directory)
    if len(os.listdir(directory)):
        print('"{}" directory is NOT empty.'.format(directory))
        exit()  # Should raise error here
    os.chdir(directory)


if __name__ == "__main__":
    main()
