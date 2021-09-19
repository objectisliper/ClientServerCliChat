import requests

from datetime import datetime


def main():
    comments = requests.get('https://api.pushshift.io/reddit/comment/search').json()['data']
    comments = sorted(comments, key=lambda key: key['created_utc'])
    comments = [f"{datetime.fromtimestamp(comment.get('created_utc'))}: {comment.get('body')}\n" for comment in comments]
    with open('reddit.txt', 'w') as file:
        file.writelines(comments)


if __name__ == '__main__':
    main()
