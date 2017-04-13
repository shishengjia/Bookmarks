from django.db import models
from django.utils.text import slugify
from users.models import UserProfile
from django.core.urlresolvers import reverse


class Image(models.Model):
    user = models.ForeignKey(UserProfile, related_name='images_created', blank=True)
    users_like = models.ManyToManyField(UserProfile, related_name='images_liked', blank=True)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    url = models.URLField()
    image = models.ImageField(upload_to='images/%Y/%m/%d')
    description = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True, db_index=True)

    def __str__(self):
        return self.title

    # def save(self, *args, **kwargs):
    #     """
    #     保存的时候为自动为图片添加slug
    #     """
    #     if not self.slug:
    #         # automatically generate the image slug for the given title when no slug is provided
    #         self.slug = slugify(self.title)
    #     super(Image, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('image:detail', args=[self.id])
