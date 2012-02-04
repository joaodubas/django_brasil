# encoding: utf-8
from django.db import models
from django.template.defaultfilters import slugify


class Text(models.Model):
    title = models.CharField(verbose_name=u'título', max_length=128)
    slug = models.SlugField(verbose_name=u'slug', max_length=128)

    def _slugify_title(self):
        i = 1
        self.slug = temp = slugify(self.title)

        while Text.objects.filter(slug=self.slug).count():
            self.slug = '%s_%d' % (temp, i)
            i += 1

    def save(self, *args, **kwargs):
        if not self.pk:
            self._slugify_title()
        super(Text, self).save(*args, **kwargs)


class Photo(models.Model):
    text = models.ForeignKey(Text, verbose_name='texto')
    image = models.ImageField(verbose_name='imagem',
            upload_to=lambda i, f: '%s/%s' % (i.text.slug, f.split('/')[-1]))
    added = models.DateTimeField(auto_now_add=True)

    class Meta:
        get_latest_by = 'added'
