import pprint
import sys

from logger.logger import logCrawlProgress
from sqlite.command import get_post_id_in_hours

sys.path.append('./src/crawler')
from crawler.facade import crawTaipeiHouseList


def sendNewRentPost():
    def filter_posttime_in_hours(houseList):
        return [house for house in houseList if '分鐘' in house['posttime']]

    post_list = crawTaipeiHouseList(filter_posttime_in_hours)
    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(post_list)
    # pp.pprint([house['posttime'] for house in post_list])

    post_ids = [int(p.post_id) for p in post_list]
    post_id_sent = get_post_id_in_hours()
    new_post_ids = list(set(post_ids).difference(set(post_id_sent)))

    # get detail of new_post_ids
    to_send = []
    for new_post_id in new_post_ids:
        # detail = crawHouseDetail(new_post_id)
        to_send.append(detail)

    # format in line message format
    # to_send = [toLineNotifyView(houseObj) for houseObj in to_send]

    # # transfer to Line message view
    try:
        pass
        # send_message(to_send)
        # # send messa succeed
        # insert_post_ids(new_post_ids)
    except:
        logCrawlProgress('send message or insert database failed')


# /crawler
def crawHouseDetail(post_id):
    pass


def toLineNotifyView(house):
    props_591 = [
        'kind_name', 'address', 'post_id', 'role_name', 'nick_name',
        'location', 'floorStr', 'price', 'post_id'
    ]

    return house


def line_formator(prop, prop_val):
    template = {
        'kind_name': f'房型: {prop_val}',
        'address': f'地點資訊: {prop_val}',
        'price': f'價錢: {prop_val}',
        'host': f'屋主資訊: {prop_val}',
        'link': f'網站連結: https://rent.591.com.tw/home/{prop_val}',
    }
    if prop not in template.keys():
        return f'{prop}: {prop_val}'
    return template[prop]


sendNewRentPost()