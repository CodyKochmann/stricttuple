from distutils.core import setup

setup(
  name = 'stricttuple',
  packages = ['stricttuple'], # this must be the same as the name above
  version = '2023.8.18',
  install_requires = ["prettytable"],
  description = 'rule based data containers',
  author = 'Cody Kochmann',
  author_email = 'kochmanncody@gmail.com',
  url = 'https://github.com/CodyKochmann/stricttuple',
  download_url = 'https://github.com/CodyKochmann/stricttuple/tarball/2023.8.18',
  keywords = ['stricttuple', 'namedtuple', 'tuple', 'design', 'contract', 'assurance', 'strict', 'rule', 'typedtuple'],
  classifiers = [],
)
