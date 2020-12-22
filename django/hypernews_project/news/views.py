from django.shortcuts import render, redirect, reverse
from django.views import View
from django.http import HttpResponse

import json
from time import time
import random
from datetime import datetime

from hypernews.settings import NEWS_JSON_PATH
from .utils import get_news, edit_news

with open(NEWS_JSON_PATH, 'r') as news_json:
    news_list = json.load(news_json)


class StartPage(View):
    def get(self, request, *args, **kwargs):
        return redirect('/news/')


class NewsPage(View):

    def get(self, request, *args, **kwargs):
        context = {'news': news_list}

        filter_query = request.GET.get('q')
        if filter_query:
            news = list(filter(lambda news: filter_query in news['title'].lower(), news_list))
            context['news'] = news

        return render(request, 'news/all_news.html', context=context)


class NewsDetails(View):

    def get(self, request, link, *args, **kwargs):
        context = {'news': get_news(news_list, link)}

        return render(request, 'news/news_info.html', context=context)


class CreateNews(View):

    def get(self, request):
        return render(request, 'news/create_news_form.html')

    def post(self, request):
        random.seed(time())
        link = int(random.random() * 10000)
        created = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        title = request.POST.get('title')
        text = request.POST.get('text')
        news = {'created': created, 'text': text, 'title': title, 'link': link}
        news_list.append(news)
        with open(NEWS_JSON_PATH, 'w') as news_json:
            news_json.write(json.dumps(news_list))
        return redirect('/news/')


class DeleteNews(View):

    def get(self, request, link):
        for i in range(len(news_list)):
            if news_list[i]['link'] == int(link):
                news_list.pop(i)

        with open(NEWS_JSON_PATH, 'w') as news_json:
            news_json.write(json.dumps(news_list))
        return redirect('/news/')

class EditNews(View):

    def get(self, request, link):
            context = {'news': get_news(news_list, link)}

            return render(request, 'news/edit_news_form.html', context=context)

    def post(self, request, link):
        new_title = request.POST.get('title')
        new_text = request.POST.get('text')
        edit_news(news_list, link, new_title, new_text)
        with open(NEWS_JSON_PATH, 'w') as news_json:
            news_json.write(json.dumps(news_list))
        return redirect(reverse('news_detail_url', kwargs={'link': link}))





