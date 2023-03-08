# Ansible filter plug-ins

A public repository with a number of custom filter plug-ins for Ansible. At the moment includes the following:

* **sitemapxml2dict:** filter plug-in that takes a [valid sitemap in XML format](https://www.sitemaps.org/protocol.html) and transforms it into a list of dictionaries, each one corresponding to a `url` and having a key for each child tag (`loc`, `lastmod`, `changefreq` and `priority`) and the same value. It has the option to validate the data retrieved from the XML file (default behaviour is not to).

To use them, just place the Python file inside a `filter_plugins/` sub-directory where your playbook resides, or use the `filter_plugins` configuration option in your `ansible.cfg` configuration file to instruct Ansible about their location (e.g. `filter_plugins = filter_plugins`).
