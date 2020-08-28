import re

from django.db import models

from gobotany.core.models import Pile, PileGroup

# The "Page" classes are for organizing information for various page types
# in order to build Haystack/Solr search engine indexes for them.

class PlainPage(models.Model):
    """Outline of the contents of a plain, miscellaneous page. Examples of
    these include the non-glossary 'Help' pages, the Teaching page, etc.
    """
    title = models.CharField(max_length=100)
    url_path = models.CharField(max_length=100)
    search_text = models.TextField()
    videos = models.ManyToManyField('core.Video')

    class Meta:
        verbose_name = 'plain page'
        verbose_name_plural = 'plain pages'

    def __str__(self):
        return '%s' % self.title


def _get_search_suggestions(input_list):
    """Return search suggestions for a Simple Key page. Attempt to
    reasonably extract parts of a list of input strings for inclusion
    as suggestions.
    """
    suggestions = []
    for input_string in input_list:
        suggestions.extend(re.split('(\, )?(and )?(for )?(with )?',
                                    input_string))
    # Remove junk pieces from after the split.
    suggestions = [suggestion.lower() for suggestion in suggestions
                   if suggestion not in [None, '', ' ', ', ', 'and ', 'for ',
                                         'with ']
                  ]
    # Omit long suggestions.
    MAX_SUGGESTION_LENGTH = 30
    suggestions = [suggestion for suggestion in suggestions
                   if len(suggestion) < MAX_SUGGESTION_LENGTH]
    # Remove some more words and characters.
    WORDS_TO_REMOVE = ['all', 'others', 'other', 'long', 'plus', 'herbaceous',
                       '"']
    for word in WORDS_TO_REMOVE:
        suggestions = [suggestion.replace(word, '')
                       for suggestion in suggestions]
    # Strip spaces.
    suggestions = [suggestion.strip() for suggestion in suggestions]
    # Omit empty strings.
    suggestions = [suggestion for suggestion in suggestions
                   if suggestion != '']
    # Omit suggestions that begin with certain words.
    OMIT_PREFIXES = ['plants', 'relatives', 'related', 'no', 'lacking',
                     'leaves', 'stems', 'obvious']
    for omit_prefix in OMIT_PREFIXES:
        suggestions = [suggestion for suggestion in suggestions
                       if suggestion.find(omit_prefix) != 0]
    # Omit duplicates.
    suggestions = list(set(suggestions))
    return suggestions


class GroupsListPage(models.Model):
    """Outline of the contents of the first Simple Key page: a list of
    plant groups.
    """
    title = models.CharField(max_length=100)
    main_heading = models.CharField(max_length=100)
    groups = models.ManyToManyField(PileGroup)

    class Meta:
        verbose_name = 'groups list page'
        verbose_name_plural = 'groups list pages'

    def __str__(self):
        return '%s' % self.title

    def search_suggestions(self):
        """Helper function to supply search suggestions for the importer."""
        suggestions = _get_search_suggestions([self.title])
        return suggestions


class SubgroupsListPage(models.Model):
    """Outline of the contents of a second-level Simple Key page:
    a list of plant subgroups.
    """
    title = models.CharField(max_length=100)
    main_heading = models.CharField(max_length=100)
    group = models.ForeignKey(PileGroup, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'subgroups list page'
        verbose_name_plural = 'subgroups list pages'

    def __str__(self):
        return '%s' % self.title

    def search_suggestions(self):
        """Helper function to supply search suggestions for the importer."""
        suggestions = _get_search_suggestions(
            [self.group.friendly_name, self.group.friendly_title])
        return suggestions


class SubgroupResultsPage(models.Model):
    """Outline of the contents of a third-level Simple Key page:
    the results page, with questions, for a subgroup.
    """
    title = models.CharField(max_length=200)
    main_heading = models.CharField(max_length=200)
    subgroup = models.ForeignKey(Pile, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'subgroup results page'
        verbose_name_plural = 'subgroup results pages'

    def __str__(self):
        return '%s' % self.title

    def search_suggestions(self):
        """Helper function to supply search suggestions for the importer."""
        suggestions = _get_search_suggestions(
            [self.subgroup.friendly_name, self.subgroup.friendly_title])

        return suggestions
