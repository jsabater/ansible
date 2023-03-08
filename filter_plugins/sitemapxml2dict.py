#!/usr/bin/env python
# -*- coding: utf-8 -*-

# (c) 2023, Jaume Sabater <jsabater@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


from ansible.errors import AnsibleFilterError, AnsibleFilterTypeError, AnsibleUndefinedVariable
from jinja2.exceptions import UndefinedError
from ansible.module_utils._text import to_native
from xml.etree import ElementTree
from datetime import date
from urllib.parse import urlparse


class FilterModule(object):
    """ XML sitemap to list of dicts filter """

    __changefreq = ['always', 'hourly', 'daily', 'weekly', 'monthly', 'yearly', 'never']

    def filters(self):
        return {
            'sitemapxml2dict': self.sitemapxml2dict
        }

    def _validate_lastmod(self, field):
        """ The date of last modification of the page. This date should be in W3C Datetime format.
        This format allows you to omit the time portion, if desired, and use YYYY-MM-DD. """
        try:
            date.fromisoformat(field)
        except ValueError:
            raise ValueError("Incorrect last modified date format")

    def _validate_loc(self, field):
        """ URL of the page. This URL must begin with the protocol (such as http) and end with a trailing slash,
        if your web server requires it. This value must be less than 2,048 characters. """
        try:
            urlparse(field)
        except ValueError:
            raise ValueError("Incorrect URL format")

    def _validate_priority(self, field):
        """ The priority of this URL relative to other URLs on your site. Valid values range from 0.0 to 1.0. """
        try:
            float(field)
        except ValueError:
            raise ValueError("Incorrect priority value")

    def _validate_changefreq(self, field):
        """ How frequently the page is likely to change. This value provides general information to search engines
        and may not correlate exactly to how often they crawl the page. Valid values are: 'always', 'hourly',
        'daily', 'weekly', 'monthly', 'yearly' and 'never'. """
        if field not in self.__changefreq:
            raise ValueError("Incorrect change frequency value")

    def sitemapxml2dict(self, sitemapxml, validate=False):
        """ Takes a sitemap in XML format and transforms it into a list of
        dictionaries, each one corresponding to a `url` and having a key for
        each tag and the same value """

        ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        sitemap = []

        try:
            urlset = ElementTree.fromstring(sitemapxml)

            for url in urlset.findall('sm:url', ns):

                # Extract values (all XML values are strings)
                loc = url.find('sm:loc', ns).text
                priority = url.find('sm:priority', ns).text
                changefreq = url.find('sm:changefreq', ns).text
                lastmod = url.find('sm:lastmod', ns).text

                # Validate values if requested
                if validate:
                    self._validate_loc(loc)
                    self._validate_priority(priority)
                    self._validate_changefreq(changefreq)
                    self._validate_lastmod(lastmod)

                sitemap.append({
                    'loc': loc,
                    'priority': priority,
                    'changefreq': changefreq,
                    'lastmod': lastmod
                })

        except ElementTree.ParseError:
            # See: https://docs.python.org/3/library/xml.etree.elementtree.html#exceptions
            raise AnsibleFilterError("Incorrect format detected while parsing the XML file")
        except ValueError:
            raise AnsibleFilterTypeError("Incorrect value in an XML tag")
        except UndefinedError as e:
            raise AnsibleUndefinedVariable("Undefined variable exception: %s" % to_native(e))
        except Exception as e:
            raise AnsibleFilterError("Unhandled exception: %s" % to_native(e))

        return sitemap
