

def get_news(news_list, link: str):
    for news in news_list:
        if news['link'] == int(link):
            return news

    return None


def edit_news(news_list, link, new_title, new_text):
    for news in news_list:
        if news['link'] == int(link):
            news['title'] = new_title
            news['text'] = new_text
