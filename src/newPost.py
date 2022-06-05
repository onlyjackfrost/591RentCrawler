from postgres.command import get_post_ids

from crawler.facade import crawNewTaipeiLocationsHouseList, crawTaipeiHouseList
from util import filter_sent_post


def filter_posttime_in_hours(houseList):
    return [
        house for house in houseList
        if ('分鐘' in house['posttime'] or '小時' in house['posttime'])
        and 'post_id' in house.keys()
    ]

def group_message(taipei_posts, new_taipei_posts, high_price_posts):
    group_messages = {}
    taipei_post_messages = [toLineNotifyView(post) for post in taipei_posts]
    taipei_post_ids = [post['post_id'] for post in taipei_posts]
    group_messages['taipei'] = {'messages':taipei_post_messages, 'post_ids':taipei_post_ids}

    new_taipei_post_messages = [toLineNotifyView(post) for post in new_taipei_posts]
    new_taipei_post_ids = [post['post_id'] for post in new_taipei_posts]
    group_messages['new_taipei'] = {'messages':new_taipei_post_messages, 'post_ids':new_taipei_post_ids}

    high_price_post_messages = [toLineNotifyView(post) for post in high_price_posts]
    high_price_post_ids = [post['post_id'] for post in high_price_posts]
    group_messages['high_price'] = {'messages':high_price_post_messages, 'post_ids':high_price_post_ids}
    return group_messages

def getNewRentPost():
    taipei_posts = crawTaipeiHouseList(filter_posttime_in_hours)

    new_taipei_posts = crawNewTaipeiLocationsHouseList(
        filter_posttime_in_hours, locations=[26, 43, 38, 37, 44, 34, 27, 47])
    # 板橋 三重 中和 永和 新莊 新店 汐止 蘆洲
    
    high_price_options = {'multiPrice':'30000_40000'}
    high_price_posts = []
    high_price_posts_taipei = crawTaipeiHouseList(filter_posttime_in_hours, options=high_price_options)
    high_price_posts_new_taipei = crawNewTaipeiLocationsHouseList(
        filter_posttime_in_hours, locations=[26, 43, 38, 37, 44, 34, 27, 47],  options=high_price_options)
    high_price_posts = high_price_posts + high_price_posts_taipei + high_price_posts_new_taipei

    all_posts = taipei_posts+ new_taipei_posts + high_price_posts_taipei + high_price_posts_new_taipei
    post_ids = [p['post_id'] for p in all_posts]
    post_id_sent = get_post_ids(post_ids)

    taipei_posts = filter_sent_post(taipei_posts, post_id_sent)
    new_taipei_posts = filter_sent_post(taipei_posts, post_id_sent)
    high_price_posts = filter_sent_post(taipei_posts, post_id_sent)

    group_messages = group_message(taipei_posts, new_taipei_posts, high_price_posts)
    return group_messages


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
