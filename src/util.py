def filter_sent_post(posts, sent_post_ids):
    return [post for post in posts if post['post_id'] not in sent_post_ids]

def get_message_destination(message_key):
    if message_key == 'taipei':
        return 'C9e6b90b821ffe626e24e2e9b1817367f'
    elif message_key == 'new_taipei':
        return 'C601eeef69fa45935ec45b031374a30bf'
    elif message_key == 'high_price':
        return 'C29bdc79e49b8c8a32e75655c94af0c58'
    else:
        return None