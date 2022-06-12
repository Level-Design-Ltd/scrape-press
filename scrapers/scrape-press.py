import csv
import json
import urllib
import re
import pandas as pd
from bs4 import BeautifulSoup

postList = []
hdr = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}

# Collect the list of search terms from the file system
with open('../sources/pages2.csv', 'r') as urls_file:
    urls_csv = csv.reader(urls_file)
    first = True

    # Start iterating through the rows
    for row in urls_csv:

        # Skip the title row (titles)
        if first:
            first = False
            continue

        # Add the rest
        url = str(row[0])
        # url = content.strip()

        if len(url) > 0:
            req = urllib.request.Request(url, headers=hdr)
            try:
                response = urllib.request.urlopen(req)
                html_string = response.read()
                soup = BeautifulSoup(markup=html_string, features='lxml')
                wp_post_id = ''
                post_class_page = ''
                post_class = ''
                meta_description = ''
                facebook_title = ''
                facebook_description = ''
                facebook_image = ''
                twitter_title = ''
                twitter_description = ''
                twitter_image = ''

                # Content
                if soup.find('title'):
                    title = soup.find('title').text.strip()
                if soup.select_one("#main-content"):
                    all_content = soup.select_one(
                        "#main-content").decode_contents().replace("<p>\n</p>", '')
                if soup.find('div', {'class': 'wp-block-image'}):
                    featured_image = soup.find(
                        'div', {'class': 'wp-block-image'}).img.attrs['src']
                if soup.find('span', {'class': 'block-author-byline__name'}):
                    author = soup.find(
                        'span', {'class': 'block-author-byline__name'})

                # Meta
                if soup.find("body", {"class": re.compile('.*page-id-.*')}):
                    body_class = soup.select_one(
                        'body[class*="page-id-"]')['class']
                    if (body_class[3] in body_class):
                        post_class_page = body_class[1]
                        post_class = body_class[2]
                        postid = body_class[2].replace("page-id-", '')
                        wp_post_id = postid

                if soup.find('script', {'class': 'yoast-schema-graph'}):
                    empty = []
                    count = 0
                    yoast_schema = json.loads(
                        soup.find('script', {'class': 'yoast-schema-graph'}).get_text(strip=True))
                    if ("@graph" in yoast_schema):
                        while count < len(yoast_schema['@graph']):
                            if (yoast_schema['@graph'][3] in yoast_schema['@graph']):
                                date_published = yoast_schema['@graph'][3]
                            count += 1

                if soup.find('title'):
                    meta_title = soup.find('title').text.strip()
                if soup.find('meta', attrs={'name': 'description'}):
                    meta_description = soup.find(
                        'meta', attrs={'name': 'description'}).attrs['content']

                # Social Meta
                if soup.find('meta', property='og:title'):
                    facebook_title = soup.find(
                        'meta', property='og:title').attrs['content']
                if soup.find('meta', property='og:description'):
                    facebook_description = soup.find(
                        'meta', property='og:description').attrs['content']
                if soup.find('meta', property='og:image'):
                    facebook_image = soup.find(
                        'meta', property='og:image').attrs['content']
                if soup.find('meta', attrs={'name': 'twitter:title'}):
                    twitter_title = soup.find(
                        'meta', attrs={'name': 'twitter:title'}).attrs['content']
                if soup.find('meta', attrs={'name': 'twitter:description'}):
                    twitter_description = soup.find(
                        'meta', attrs={'name': 'twitter:description'}).attrs['content']
                if soup.find('meta', attrs={'name': 'twitter:image'}):
                    twitter_image = soup.find(
                        'meta', attrs={'name': 'twitter:image'}).attrs['content']

                singlePost = [
                    {
                        'wp_post_id': wp_post_id,
                        'post_class': post_class,
                        'title': title,
                        'content': all_content,
                        'date_published': date_published,
                        'meta_title': meta_title,
                        'meta_description': meta_description,
                        'facebook_title': facebook_title,
                        'facebook_description': facebook_description,
                        'facebook_image': facebook_image,
                        'twitter_title': twitter_title,
                        'twitter_description': twitter_description,
                        'twitter_image': twitter_image,
                    }
                ]

                if (singlePost[0]['post_class'] != '' and post_class_page == 'page'):
                    print(title, "----------", wp_post_id)
                    postList.append(singlePost)

                df = pd.DataFrame(postList)
                df.to_json('../data/pages2.json', date_format='iso')

            except urllib.error.HTTPError as e:
                print("Server Offline")
            except urllib.error.URLError as e:
                print("Server Offline")
