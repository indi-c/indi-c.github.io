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
title: Free Learning - {title}
---
'''

# make a new file for each domain in _learning/ by the name of the domain id 
# by using the html_template and filling in the title with the domain title
# append the freelearningcontent include for each field in the domain to the file, 
# with the url being the field id and the title being the field title and the description being the field description
# also make a new folder for each domain in _learning/domains/ by the name of the domain id
for domain in domains:
    domain_id = domain['id']
    domain_title = domain['title'].title() if domain['title'] != domain['title'].upper() else domain['title']
    domain_fields = domain_to_fields[domain_id]

    # make a new folder for each domain in _learning/ by the name of the domain id
    os.makedirs(f'_learning/{domain_id}', exist_ok=True)

    with open(f'_learning/{domain_id}.html', 'w') as f:
        f.write(html_template.format(title=domain_title))
        f.write(f'{{% include freelearningtopictitle.html title="{domain_title}" description="{domain["description"]}" %}}\n')

        for field in domain_fields:
            field_id = field['id']
            field_title = field['title'].title() if field['title'] != field['title'].upper() else field['title']
            field_brief = field['brief']
            f.write(f'{{% include freelearningcontent.html url="{field_id}" title="{field_title}" brief="{field_brief}" %}}\n')

# repeat the above for each field in _learning/fields/ by the name of the field id
for field in fields:
    field_id = field['id']
    field_domain = field['domain']
    field_title = field['title'].title() if field['title'] != field['title'].upper() else field['title']
    field_description = field['description']
    field_topics = field_to_topics[field_id]

    # make a new folder for each field in _learning/{domain} by the name of the field id
    os.makedirs(f'_learning/{field_domain}/{field_id}', exist_ok=True)

    with open(f'_learning/{field_domain}/{field_id}.html', 'w') as f:
        f.write(html_template.format(title=field_title))
        f.write(f'{{% include freelearningtopictitle.html title="{field_title}" description="{field_description}" %}}\n')
        for topic in field_topics:
            topic_id = topic['id']
            topic_title = topic['title'].title() if topic['title'] != topic['title'].upper() else topic['title']
            topic_brief = topic['brief']
            f.write(f'{{% include freelearningcontent.html url="{topic_id}" title="{topic_title}" brief="{topic_brief}" %}}\n')

# repeat the above for each topic in _learning/topics/ by the name of the topic id but populating with information from resources.yml
resources = yaml.safe_load(open('_data/freelearning/resources.yml'))
for topic in topics:
    topic_id = topic['id']
    topic_field = topic['field']
    topic_title = topic['title'].title() if topic['title'] != topic['title'].upper() else topic['title']
    topic_description = topic['description']
    topic_resources = [resource for resource in resources if topic_id in resource['topics']]
    topic_domain = next((field['domain'] for field in fields if field['id'] == topic_field), None)

    with open(f'_learning/{topic_domain}/{topic_field}/{topic_id}.html', 'w') as f:
        f.write(html_template.format(title=topic_title))
        f.write(f'{{% include freelearningtopictitle.html title="{topic_title}" description="{topic_description}" %}}\n')
        for resource in topic_resources:
            resource_id = resource['id']
            resource_title = resource['title'].title() if resource['title'] != resource['title'].upper() else resource['title']
            resource_brief = resource['brief']
            resource_url = resource['url']
            f.write(f'{{% include freelearningcontent.html url="{resource_url}" title="{resource_title}" brief="{resource_brief}" %}}\n')