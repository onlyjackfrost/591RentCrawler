from postgres.command import get_post_ids

from crawler.facade import crawTaipeiHouseList


def getNewRentPost():
    def filter_posttime_in_hours(houseList):
        return [
            house for house in houseList
            if ('分鐘' in house['posttime'] or '小時' in house['posttime'])
            and 'post_id' in house.keys()
        ]

    post_list = crawTaipeiHouseList(filter_posttime_in_hours)
    post_ids = [p['post_id'] for p in post_list]
    post_id_sent = get_post_ids(post_ids)
    new_posts = [
        post for post in post_list if post['post_id'] not in post_id_sent
    ]

    # format in line message format
    print(len(new_posts))
    messages = [toLineNotifyView(new_post) for new_post in new_posts]
    new_post_ids = [post['post_id'] for post in new_posts]
    return messages, new_post_ids


def toLineNotifyView(house):
    messages = []
    for category in category_order:
        props = [
            ele['prop'] for ele in props_and_categories
            if ele['category'] == category
        ]
        prop_val = ', '.join([str(house[prop]) for prop in props])
        messages.append(line_formator(category, prop_val))

    return '\n\r'.join(messages)


props_and_categories = [
    {
        'prop': 'kind_name',
        'category': 'kind_name'
    },
    {
        'prop': 'address',
        'category': 'address'
    },
    {
        'prop': 'post_id',
        'category': 'link'
    },
    # {
    #     'prop': 'role_name',
    #     'category': 'host'
    # },
    {
        'prop': 'nick_name',
        'category': 'host'
    },
    {
        'prop': 'location',
        'category': 'address'
    },
    {
        'prop': 'floorStr',
        'category': 'address'
    },
    {
        'prop': 'price',
        'category': 'price'
    },
]
category_order = ['kind_name', 'address', 'price', 'host', 'link']


def line_formator(category, prop_val):
    category_message_template = {
        'kind_name': f'房型: {prop_val}',
        'address': f'地點資訊: {prop_val}',
        'price': f'價錢: {prop_val}',
        'host': f'屋主資訊: {prop_val}',
        'link': f'網站連結: https://rent.591.com.tw/home/{prop_val}',
    }
    if category not in category_message_template.keys():
        return f'{category}: {prop_val}'
    return category_message_template[category]
