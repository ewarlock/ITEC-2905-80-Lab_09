from django.db import models
from django.contrib.auth.models import User # django built in User model

from django.core.files.storage import default_storage

# Create your models here.

class Place(models.Model):
    # django built in User model foreign key
    user = models.ForeignKey('auth.User', null=False, on_delete=models.CASCADE) # use string to name other table. 
    # on_delete cascade means delete all associated info if user deleted
    name = models.CharField(max_length=200)
    visited = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True) # less limit than charfield as much text as wanted
    date_visited = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='user_images/', blank=True, null=True)

    # saving image and deleting it...
    # override django's save method
    def save(self, *args, **kwargs):
        old_place = Place.objects.filter(pk=self.pk).first()
        if old_place and old_place.photo:
            if old_place.photo != self.photo:
                self.delete_photo(old_place.photo)
        # if there is old place, and it has photo, and new photo not same as old photo, delete old photo
        super().save(*args, **kwargs)

    def delete_photo(self, photo):
        # delete the photo if it exists
        if default_storage.exists(photo.name):
            default_storage.delete(photo.name)

    def delete(self, *args, **kwargs):
        # delete the photo if the place is deleted
        if self.photo:
            self.delete_photo(self.photo)
        
        super().delete(*args, **kwargs)

    def __str__(self):
        photo_str = self.photo.url if self.photo else 'no photo'
        notes_str = self.notes[100:] if self.notes else 'no notes' # truncate to 100 chars
        return f'{self.pk}: {self.name}, visited? {self.visited} on {self.date_visited}. Notes: {notes_str}\nPhoto {photo_str}'
