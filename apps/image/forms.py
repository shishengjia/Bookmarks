from django import forms
from .models import Image
from urllib import request
from django.core.files.base import ContentFile
from django.utils.text import slugify


class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'url', 'description')
        # 隐藏url字段
        widgets = {
            'url': forms.HiddenInput,
        }

    def clean_url(self):
        """
        clean_<fieldname>()
        This method is executed for each field, if present, when you call is_valid() on a form instance.
        to check the validation of url
        """
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg', 'png']
        # 提取图片url的后缀名
        extension = url.rsplit('.', 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError('The given URL does not match valid image extensions.')
        return url

    def save(self, force_insert=False, force_update=False, commit=True):
        """
        download the image file by overriding the save() method of model form
        perform this task every time the form is saved.
        """
        # create a new image instance by calling the save() method of the form with commit=False
        image_instance = super(ImageCreateForm, self).save(commit=False)

        image_instance_url = self.cleaned_data['url']
        image_instance_name = '{}.{}'.format(slugify(image_instance.title), image_instance_url.rsplit('.', 1)[1].lower())

        response = request.urlopen(image_instance_url)

        # call the save() method of the image field to save the file to the media directory
        image_instance.image.save(image_instance_name, ContentFile(response.read()), save=False)
        if commit:
            image_instance.save()
        return image_instance
