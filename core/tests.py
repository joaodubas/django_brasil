# encoding: utf-8
import os

from django.conf import settings
from django.core.files import File
from django.template.defaultfilters import slugify
from django.test import TestCase
from core.models import Text

ROOT = lambda *x: os.path.join(os.path.dirname(os.path.abspath(__file__)), *x)
IMAGE = ROOT('test_data', 'image.jpg')


class TextTest(TestCase):
    def test_text_has_slug(self):
        text = Text(title='Ola mundo')
        text.save()
        self.assertEqual(text.slug, slugify(text.title))

    def test_slug_is_unique(self):
        text_first = Text(title='Ola mundo')
        text_first.save()
        self.assertEqual(text_first.slug, slugify(text_first.title))

        text_second = Text(title=text_first.title)
        text_second.save()
        self.assertEqual(text_second.slug, '%s_1' % slugify(text_second.title))

        text_third = Text(title=text_first.title)
        text_third.save()
        self.assertEqual(text_third.slug, '%s_2' % slugify(text_third.title))

class PhotoTest(TestCase):
    def test_photo_is_uploaded_to_right_place(self):
        text = Text(title='Ola mundo')
        text.save()

        text.photo_set.create(image=File(open(IMAGE)))
        photo = text.photo_set.latest()
        expect_upload_dir = os.path.join(settings.MEDIA_ROOT, text.slug, 'image.jpg')
        self.assertEqual(photo.image.path, expect_upload_dir)
