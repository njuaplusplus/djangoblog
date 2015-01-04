#!/usr/local/bin/python
# coding=utf-8

from django.db import models
from django.utils.translation import ugettext as _
# from markdown import markdown
import markdown
from django.contrib.auth.models import User
from uuslug import uuslug
from django import forms
from pagedown.widgets import PagedownWidget
# from bootstrap3_datetime.widgets import DateTimePicker
from datetimewidget.widgets import DateTimeWidget

class Category(models.Model) :
    """Category Model"""
    title = models.CharField(
        verbose_name = _(u'名称'),
        help_text = _(u' '),
        max_length = 255
    )
    slug = models.SlugField(
        verbose_name = _(u'Slug'),
        help_text = _(u'Uri identifier.'),
        max_length = 255,
        unique = True
    )

    class Meta:
        app_label = _(u'blog')
        verbose_name = _(u"Category")
        verbose_name_plural = _(u"Categories")
        ordering = ['title',]

    def save(self, *args, **kwargs):
        if not self.slug.strip():
            # slug is null or empty
            self.slug = uuslug(self.title, instance=self, max_length=32, word_boundary=True)
        super(Category, self).save(*args, **kwargs)

    def __unicode__(self):
        return "%s" % (self.title,)

class MyImage(models.Model):
    ''' Image storage for the post'''
    image = models.ImageField(
        verbose_name = _(u'图片'),
        help_text = _(u' '),
        upload_to='blogs/images/%Y/%m/%d',
    )
    title = models.CharField(
        verbose_name = _(u'标题'),
        help_text = _(u' '),
        max_length = 100
    )
    description = models.TextField(
        verbose_name = _(u'描述'),
        help_text = _(u' '),
        blank = True
    )
    class Meta:
        app_label = _(u'blog')
        verbose_name = _(u"Image")
        verbose_name_plural = _(u"Images")
        ordering = ['title',]
    def __unicode__(self):
        return "%s" % (self.title,)

class Article(models.Model) :
    """Article Model"""
    title = models.CharField(
        verbose_name = _(u'标题'),
        help_text = _(u' '),
        max_length = 255
    )
    slug = models.SlugField(
        verbose_name = _(u'固定链接'),
        help_text = _(u'本文章的短网址(Uri identifier).'),
        max_length = 255,
        unique = True
    )
    cover = models.ImageField(
        verbose_name = _(u'封面'),
        help_text = _(u'若留空, 则使用默认图片'),
        upload_to='blogs/images/%Y/%m/%d',
        null = True,
        blank = True
    )
    excerpt = models.TextField(
        verbose_name = _(u'摘要'),
        help_text = _(u' '),
        blank = True
    )
    images = models.ManyToManyField(
        MyImage,
        verbose_name = _(u'图片'),
        help_text = _(u'向文章中插入图片'),
        null = True,
        blank = True
    )
    author = models.ForeignKey(User, verbose_name=_(u'作者'))
    content_markdown = models.TextField(
        verbose_name = _(u'内容 (Markdown)'),
        help_text = _(u' '),
    )
    content_markup = models.TextField(
        verbose_name = _(u'内容 (Markup)'),
        help_text = _(u' '),
    )
    categories = models.ManyToManyField(
        Category,
        verbose_name = _(u'分类'),
        help_text = _(u' '),
        null = True,
        blank = True
    )
    date_publish = models.DateTimeField(
        verbose_name = _(u'发布日期'),
        help_text = _(u' ')
    )
    is_public = models.BooleanField(verbose_name = _(u'公开博客'))
    is_approved = models.BooleanField(verbose_name = _(u'通过审核'))
    is_markuped = models.BooleanField(verbose_name = _(u'已经编译'))

    class Meta:
        app_label = _(u'blog')
        verbose_name = _(u"Article")
        verbose_name_plural = _(u"Articles")
        ordering = ['-date_publish']

    def save(self, *args, **kwargs):
        if not self.slug.strip():
            # slug is null or empty
            self.slug = uuslug(self.title, instance=self, max_length=32, word_boundary=True)
        if self.is_approved is None:
            self.is_approved = False
        if self.is_public is None:
            self.is_public = False
        if self.is_markuped is None:
            self.is_markuped = False
        # self.content_markup = markdown.markdown(self.content_markdown, ['codehilite', 'attr_list'])
        super(Article, self).save(*args, **kwargs)

    def get_content_markup(self):
        if not self.is_markuped:
            self.is_markuped = True
            self.content_markup = markdown_to_html(self.content_markdown, self.images.all())
            self.save()
        return self.content_markup

    def __unicode__(self):
        return "%s" % (self.title,)

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        dateTimeOptions = {
            'todayBtn' : 'true',
        }
        widgets = {
            # 'content_markdown' : PagedownWidget(),
            # 'date_publish' : DateTimePicker(options={"format": "YYYY-MM-DD HH:mm", "pickSeconds": False, "language": 'zh-cn', }),
            'date_publish' : DateTimeWidget(usel10n=True, bootstrap_version=3, options = dateTimeOptions),
            'title' : forms.TextInput(attrs={'class':'form-control'}),
            'slug' : forms.TextInput(attrs={'class':'form-control'}),
            'excerpt' : forms.Textarea(attrs={'class':'form-control'}),
            'categories' : forms.SelectMultiple(attrs={'class':'form-control'}),
            'images' : forms.SelectMultiple(attrs={'class':'form-control'}),
        }
        exclude = ['content_markup', 'author', 'is_approved', 'is_markuped',]

from django.contrib.auth.models import User

# Create your models here.

class User_Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    duoshuo_id = models.IntegerField(default=0)
    token = models.IntegerField(default=0)
    avatar = models.URLField(blank=True, null=True)

    def __unicode__(self):
        return self.user.username

def markdown_to_html(text, images):
    '''Compile the text into html
    '''
    md = markdown.Markdown(extensions=['codehilite', 'attr_list'])
    for img in images:
        md.references[img.title] = (img.image.url, img.title)
    print md.references
    return md.convert(text)
