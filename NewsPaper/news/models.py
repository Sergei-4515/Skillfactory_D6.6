from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from django.urls import reverse



class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        articles_rating = \
            Post.objects.filter(author_id=self.id).aggregate(Sum('rating_news')).get('rating_news__sum') * 3
        #print(articles_rating)
        comments_rating = \
            Comment.objects.filter(author_id=self.id).aggregate(Sum('comment_rating')).get('comment_rating__sum')
        #print(comments_rating)
        comments_articles_rating = \
            Comment.objects.filter(post__author=self).aggregate(Sum('comment_rating')).get('comment_rating__sum')
        #print(comments_articles_rating)

        self.rating = articles_rating + comments_rating + comments_articles_rating
        self.save()

    def __str__(self):
        return f'{self.author.username}'


sport = 'SP'
politics = 'PO'
education = 'ED'
culture = 'CU'

TOPICS = [
    (sport, 'СПОРТ'),
    (politics, 'ПОЛИТИКА'),
    (education, 'ОБРАЗОВАНИЕ'),
    (culture, 'КУЛЬТУРА')
]


class Category(models.Model):
    topic = models.CharField(max_length=2, choices=TOPICS, default=politics, unique=True)

    def __str__(self):
        return self.topic.title()

news = 'NW'
article = 'AR'

SELECTION = [
    (news, 'Новость'),
    (article, 'Статья')
]


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    article_news = models.CharField(max_length=2, choices=SELECTION, default=news)
    date_in = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating_news = models.IntegerField(default=0)
    category = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.rating_news += 1
        self.save()

    def dislike(self):
        self.rating_news -= 1
        self.save()

    def preview(self):
        return self.text[0:124] + '...'

    # def get_absolute_url(self):
    #     return reverse('post_detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.title.title()}:{self.text.title()}:{self.date_in}'




class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField(blank=False)
    comment_time_in = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()