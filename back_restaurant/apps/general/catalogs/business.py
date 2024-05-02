from django.db import models


class RatingChoices(models.IntegerChoices):
    RATING_0 = 0, "Rating 0"
    RATING_1 = 1, "Rating 1"
    RATING_2 = 2, "Rating 2"
    RATING_3 = 3, "Rating 3"
    RATING_4 = 4, "Rating 4"
