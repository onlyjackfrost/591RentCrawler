import time


def logCrawlProgress(info):
    timeString = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime())
    with open('GetId.log', 'at') as file:
        file.write(timeString + '  ' + info)