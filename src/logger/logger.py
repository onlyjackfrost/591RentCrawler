import os
import time

is_local = os.getenv('LOCAL')


def logCrawlProgress(info):
    if not is_local:
        print('is not local')
        return
    timeString = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime())
    with open('GetId.log', 'at') as file:
        file.write(timeString + '  ' + info)