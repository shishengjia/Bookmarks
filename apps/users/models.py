from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse


class UserProfile(AbstractUser):
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)

    def __str__(self):
        return '{}'.format(self.username)

    def get_absolute_url(self):
        return reverse('users:detail', args=[self.username])

    def get_follower_num(self):
        return Contact.objects.filter(user_to=self).count()


class Contact(models.Model):
    user_from = models.ForeignKey(UserProfile, related_name='rel_from_set')
    user_to = models.ForeignKey(UserProfile, related_name='rel_to_set')
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{} follows {}'.format(self.user_from, self.user_to)
