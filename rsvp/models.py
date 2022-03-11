from django.db import models

class Reservation(models.Model):

    first_name = models.CharField(max_length=50)
    middle_initial = models.CharField(max_length=1)
    last_name = models.CharField(max_length=50)
    full_name = models.CharField(max_length=101)
    total_attendees = models.PositiveSmallIntegerField(default=0)
    chicken = models.PositiveSmallIntegerField(default=0)
    beef = models.PositiveSmallIntegerField(default=0)
    fish = models.PositiveSmallIntegerField(default=0)
    comments = models.TextField(blank=True)


    csv_fields = (
        'last_name',
        'first_name',
        'middle_initial',
        'total_attendees',
        'chicken',
        'beef',
        'fish',
        'comments',
    )

    class Meta:
        ordering = ['full_name']

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        self.full_name = f'{self.last_name.upper()}, {self.first_name.upper()} {self.middle_initial.upper()}.'
        super().save(*args, **kwargs)