from django.db import models
from django.contrib.auth.models import User


class Director(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    @property
    def count_movies(self):
        return self.movies.all().count()


class Movie(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    duration = models.PositiveIntegerField()
    director = models.ForeignKey(Director, on_delete=models.CASCADE, related_name='movies')

    def __str__(self):
        return self.title

    @property
    def count_reviews(self):
        return self.reviews.all().count()

    @property
    def average_rating(self):
        reviews = self.reviews.all()

        if len(reviews) == 0:
            return 0

        total_stars = sum(review.stars for review in reviews)
        return total_stars / len(reviews)

    @property
    def all_reviews(self):
        reviews = Review.objects.filter(movie=self)
        return [{'id': i.id, 'text': i.text, 'stars': i.stars} for i in reviews]


class Review(models.Model):
    text = models.TextField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    stars = models.IntegerField(choices=[(1, '1 star'), (2, '2 stars'), (3, '3 stars'), (4, '4 stars'), (5, '5 stars')],
                                default=1)

    def __str__(self):
        return f'{self.text}'
