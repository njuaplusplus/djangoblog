#!/usr/local/bin/python
# coding=utf-8

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from blog.models import Category, Article
import calendar, datetime

def index(request):
    return index_page(request, 1)

def index_page(request, page_num):
    """The news index"""
    # archive_dates = Article.objects.datetimes('date_publish','month', order='DESC')
    # categories = Category.objects.all()

    article_queryset = Article.objects.all()
    paginator = Paginator(article_queryset, 5)

    try:
        articles = paginator.page(page_num)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        articles = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        articles = paginator.page(paginator.num_pages)

    return render(
        request,
        "blog/index.html",
        {
            "articles" : articles,
            # "archive_dates" : archive_dates,
            # "categories" : categories
        }
    )

def single(request, slug) :
    """A single article"""
    article = get_object_or_404(Article, slug=slug)
    # archive_dates = Article.objects.datetimes('date_publish','month', order='DESC')
    # categories = Category.objects.all()
    return render(
        request,
        "blog/post.html",
        {
            "article" : article,
            # "archive_dates" : archive_dates,
            # "categories" : categories
        }
    )

def date_archive(request, year, month) :
    """The blog date archive"""
    # this archive pages dates
    year = int(year)
    month = int(month)
    month_range = calendar.monthrange(year, month)
    start = datetime.datetime(year=year, month=month, day=1)#.replace(tzinfo=utc)
    end = datetime.datetime(year=year, month=month, day=month_range[1])#.replace(tzinfo=utc)
    archive_dates = Article.objects.datetimes('date_publish','month', order='DESC')
    categories = Category.objects.all()

    # Pagination
    page = request.GET.get('page')
    article_queryset = Article.objects.filter(date_publish__range=(start.date(), end.date()))
    paginator = Paginator(article_queryset, 5)

    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        articles = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        articles = paginator.page(paginator.num_pages)

    return render(
        request,
        "blog/article/date_archive.html",
        {
            "start" : start,
            "end" : end,
            "articles" : articles,
            "archive_dates" : archive_dates,
            "categories" : categories
        }
    )

def category_archive(request, slug):
    return category_archive_page(request, slug, 1)

def category_archive_page(request, slug, page_num):
    # archive_dates = Article.objects.datetimes('date_publish','month', order='DESC')
    # categories = Category.objects.all()
    category = get_object_or_404(Category, slug=slug)

    # Pagination
    article_queryset = Article.objects.filter(categories=category)
    paginator = Paginator(article_queryset, 5)

    try:
        articles = paginator.page(page_num)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        articles = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        articles = paginator.page(paginator.num_pages)
    return render(
        request,
        "blog/category_archive.html",
        {
            "articles" : articles,
            # "archive_dates" : archive_dates,
            # "categories" : categories,
            "category" : category
        }
    )
