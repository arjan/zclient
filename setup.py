#
# ZClient API: distutils file for distributing the library
#
# (c)2011 Arjan Scherpenisse <arjan@mediamatic.nl>
#
#
# The MIT License
#
# Copyright (c) 2011 Arjan Scherpenisse
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
#

from setuptools import setup

from zclient import __version__

setup(name='ZotonicClient',
      version=__version__,
      description="Support library for accessing Zotonic websites from Python.",
      long_description=open("README.md", "r").read(),
      author='Arjan Scherpenisse',
      author_email='arjan@scherpenisse.net',
      maintainer_email='arjan@scherpenisse.net',
      platforms='any',
      url='http://github.com/arjan/zclient',
      keywords="zotonic api web2.0 oauth",
      license='MIT',
      classifiers=["Development Status :: 3 - Alpha",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: MIT License",
                   "Programming Language :: Python",
                   "Topic :: Software Development :: Libraries :: Python Modules",
                   ],
      packages=['zclient'],
      install_requires = [
      'simplejson', 'oauth'
      ],
      entry_points = {'console_scripts': ['zclient = zclient.cli:main']}
      )
