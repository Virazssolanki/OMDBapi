from django.db import models

class Ratings(models.Model):
    source = models.CharField(max_length=50)
    rating = models.CharField(max_length=10)

    def __str__(self):
        return self.source
        
class Movie(models.Model):
    imdbID = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=255)
    year = models.CharField(max_length=4, blank=True)
    rating = models.ManyToManyField(Ratings, blank=True)

    def __str__(self):
        return '{} ({})'.format(self.title, self.year)