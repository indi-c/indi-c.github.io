import yaml
import os

domains = yaml.safe_load(open('_data/freelearning/domains.yml'))
fields = yaml.safe_load(open('_data/freelearning/fields.yml'))
topics = yaml.safe_load(open('_data/freelearning/topics.yml'))

# map each domain to its fields by using the domains id field as a key to look up fields that have a matching domain field
domain_to_fields = {}
for domain in domains:
    domain_id = domain['id']
    domain_fields = [field for field in fields if field['domain'] == domain_id]
    domain_to_fields[domain_id] = domain_fields

# map each field to its topics by using the fields id field as a key to look up topics that have a matching field field
field_to_topics = {}
for field in fields:
    field_id = field['id']
    field_topics = [topic for topic in topics if topic['field'] == field_id]
    field_to_topics[field_id] = field_topics

html_template = '''---
layout: freelearningdefault
title: {title}
---
'''

# make a new file for each domain in _learning/ by the name of the domain id 
# by using the html_template and filling in the title with the domain title
# append the freelearningcontent include for each field in the domain to the file, 
# with the url being the field id and the title being the field title and the description being the field description
# also make a new folder for each domain in _learning/domains/ by the name of the domain id
for domain in domains:
    domain_id = domain['id']
    domain_title = domain['title']
    domain_fields = domain_to_fields[domain_id]

    # make a new folder for each domain in _learning/ by the name of the domain id
    os.makedirs(f'_learning/{domain_id}', exist_ok=True)

    with open(f'_learning/{domain_id}.html', 'w') as f:
        f.write(html_template.format(title=domain_title))
        for field in domain_fields:
            field_id = field['id']
            field_title = field['title']
            field_description = field['description']
            f.write(f'{{% include freelearningcontent.html url="{field_id}" title="{field_title}" description="{field_description}" %}}\n')

# repeat the above for each field in _learning/fields/ by the name of the field id
for field in fields:
    field_id = field['id']
    field_domain = field['domain']
    field_title = field['title']
    field_description = field['description']
    field_topics = field_to_topics[field_id]

    # make a new folder for each field in _learning/ by the name of the field id
    os.makedirs(f'_learning/{field_domain}/{field_id}', exist_ok=True)

    with open(f'_learning/{field_domain}/{field_id}.html', 'w') as f:
        f.write(html_template.format(title=field_title))
        for topic in field_topics:
            topic_id = topic['id']
            topic_title = topic['title']
            topic_description = topic['description']
            f.write(f'{{% include freelearningcontent.html url="{topic_id}" title="{topic_title}" description="{topic_description}" %}}\n')