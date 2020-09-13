import re
import os

POSTS_PATH = '../_posts/'

list_of_posts = os.listdir(POSTS_PATH)

tag_template = '''---
layout: page
title: {tag_name}
permalink: /tag/{tag_name}
istag: 1
excerpt: "{tag_name}"
noindex: true
sitemap: false
---

{{% include tag.html tag=page.title %}}
'''

created_tags = {}

for post_file in list_of_posts:
    with open(POSTS_PATH + post_file, 'r') as f:
        content = f.read()
        tags_list = re.findall(r'^tags:.+$', content, flags=re.MULTILINE)

        if len(tags_list) == 0:
            continue

        tags_list = tags_list[0].replace('tags: ', '').split(' ')
        print(tags_list)

        for tag in tags_list:

            if tag in created_tags:
                continue

            with open(tag +'.md', 'w') as tag_file:
                tag_file.write(tag_template.format(tag_name = tag))
                created_tags[tag] = 1


        