from django.db import models
from django.contrib.auth.models import User
from datetime import timezone
#from application.models import *

class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):

        article_rating = sum(post.rating * 3 for post in self.post_set.all())
        comment_rating = sum(comment.rating for comment in Comment.objects.filter(post__author=self))
        comment_rating += sum(comment.rating for post in self.post_set.all() for comment in post.comment_set.all())
        self.rating = article_rating + comment_rating
        self.save()

# user1 = User.objects.create_user(username='Mike')
# user2 = User.objects.create_user(username='Joe')
#  author1 = Author.objects.create(author_id = 1, rating = 2)
#  author2 = Author.objects.create(author_id = 2, rating = 3)
# category1 = Category.objects.create(categories = 'sport')
# category2 = Category.objects.create(categories = 'world')
# category3 = Category.objects.create(categories = 'entertainment')
# category4 = Category.objects.create(categories = 'politics')
# post1 = Post.objects.create(author = author1,
#                              options = 'article',
#                              time_of_creation = timezone.utc,
#                              title = 'Title2',
#                              content_of_article = 'content of the second article',
#                              rating = 6)
# post2 = Post.objects.create(author = author2,
#                              options = 'news',
#                              time_of_creation = timezone.utc,
#                              title = 'Title1',
#                              content_of_article = 'content of the news',
#                              rating = 3)
# post3 = Post.objects.create(author = author2,
#                              options = 'article',
#                              time_of_creation = timezone.utc,
#                              title = 'Title3',
#                              content_of_article = 'content of article',
#                              rating = 4)
#
# post1.categories.add(category1)
# post1.categories.add(category2)
# post2.categories.add(category1)
#
# comment1 = Comment.objects.create(
#     user=user1,
#     post=post1,
#     comment='Comment 1',
#     date=timezone.utc,
#     rating=2,
# )
# comment2 = Comment.objects.create(
#     user=user2,
#     post=post2,
#     comment='Comment 2',
#     date=timezone.utc,
#     rating=3,
# )
# comment3 = Comment.objects.create(
#     user=user1,
#     post=post1,
#     comment='Comment 3',
#     date=timezone.utc,
#     rating=4,
# )
# comment4 = Comment.objects.create(
#     user=user2,
#     post=post2,
#     comment='Comment 4',
#     date=timezone.utc,
#     rating=5,
# )
class Category(models.Model):
    categories = models.CharField(max_length=64,
                                default="Name_of_category",
                                unique=True)


class Post(models.Model):
    # article = 'article'
    # news = 'news'

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    options = models.CharField(max_length=10, choices=[('article', 'Article'), ('news', 'News')], default='article')
    time_of_creation = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField('Category', through='PostCategory')
    title = models.CharField(max_length=255)
    content_of_article = models.TextField()
    rating = models.IntegerField(default=0)




    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f'{self.content_of_article.split()[:124]}...'




class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)


# comment5 = Comment.objects.create(
#     user = user1,
#     post = post3,
#     comment = 'comment5',
#     date = timezone.utc,
#     rating = 2
# ) did not use this one


    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


# best_user = User.objects.order_by('username').first()
# best_user.username
# best_user.author.rating
#
#
# best_post = Post.objects.order_by('-rating').first()
# best_post.time_of_creation
# best_post.author.author
# best_post.rating
# best_post.title
# best_post.preview()
#
# comments = Comment.objects.filter(post=best_post)
# for comment in comments:
#     print(comment.date, comment.user.username, comment.rating, comment.comment)