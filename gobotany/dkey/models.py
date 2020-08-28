"""Data model for the dichotomous key."""

import re

from django.db import models

# Here are the possible dkey page ranks. Note that a "subgroup" can
# stand either between a family and a genus, or between a very large
# genus and a section. The top of the hierarchy is always:
#
# top -> group -> family
#
# There are two ways that a family can bottom out in genera:
#
# family -> genus
# family -> subgroup -> genus
#
# Then there are three different ways that genera reach their species:
#
# genus -> species
# genus -> subkey -> species
# genus -> subgroup -> section -> species

def slug_to_title(slug):
    """The canonical transform between a URL slug and a dkey Page title."""
    return slug.replace('-', ' ').capitalize().replace(
        ' families', ' Families').replace(' group ', ' Group ')

class Page(models.Model):
    """A page of the dichotomous key, that can have several leads on it."""

    chapter = models.TextField(blank=True)
    title = models.TextField(unique=True)
    rank = models.TextField(db_index=True)
    text = models.TextField(blank=True)
    breadcrumb_cache = models.ManyToManyField('Page', related_name='ignore+')

    class Meta:
        verbose_name = 'dichotomous key page'
        verbose_name_plural = 'dichotomous key pages'

    def __str__(self):
        return self.title

    @property
    def sorted_leads(self):
        return self.leads.order_by('id')

class Lead(models.Model):
    """A text description that leads you down one path in the dkey."""

    page = models.ForeignKey('Page', related_name='leads',
        on_delete=models.PROTECT)
    parent = models.ForeignKey('Lead', related_name='children', null=True,
        blank=True, on_delete=models.PROTECT)
    letter = models.TextField()
    text = models.TextField()
    goto_page = models.ForeignKey('Page', related_name='leadins', null=True,
        blank=True, on_delete=models.PROTECT)
    goto_num = models.IntegerField(null=True, blank=True)
    taxa_cache = models.TextField(blank=True)

    def __str__(self):
        return '{}:{}.{}'.format(self.id, self.letter, self.goto_page_id
                                  or self.goto_num or '')

    def number(self):
        return self.letter.strip('ab')

    def sort_key(self):
        """Turn '12a' into (12, 'a') but '12' into simply (12,).

        All real leads from the database have a number and letter like
        '12a', but the artificial leads on the /family-groups/ page have
        simple integers as strings like '12'.

        """
        if not self.letter:
            return 0,
        elif self.letter[-1].isdigit():
            return int(self.letter),
        else:
            return int(self.letter[:-1]), self.letter[-1]

    def text_excerpt(self):
        """Return a short excerpt of the lead text."""
        MAX_WORDS = 7
        excerpt = [_f for _f in re.split('[;,]+', self.text) if _f][0]
        words = excerpt.split(' ')
        return ' '.join(words[0:MAX_WORDS])

class Hybrid(models.Model):
    """A paragraph describing a hybrid species."""

    number1 = models.IntegerField(null=True, blank=True)
    number2 = models.IntegerField(null=True, blank=True)
    scientific_name1 = models.TextField(db_index=True)
    scientific_name2 = models.TextField(db_index=True)
    text = models.TextField(blank=True)

class Figure(models.Model):
    number = models.IntegerField(primary_key=True)
    caption = models.TextField()

class IllustrativeSpecies(models.Model):
    group_number = models.IntegerField()
    family_name = models.TextField(db_index=True)
    species_name = models.TextField()

    class Meta:
        verbose_name_plural = 'Illustrative species'