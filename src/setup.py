"""
    https://packaging.python.org/distributing/
    https://pypi.python.org/pypi?%3Aaction=list_classifiers
    http://semver.org/

    zero or more dev releases (denoted with a ”.devN” suffix)
    zero or more alpha releases (denoted with a ”.aN” suffix)
    zero or more beta releases (denoted with a ”.bN” suffix)
    zero or more release candidates (denoted with a ”.rcN” suffix)
"""

from setuptools import setup, find_packages

setup(name='digesto-api',
          version='1.0.3',
          description='Proyecto que implementa la api del digesto institucional',
          url='https://github.com/pablodanielrey/digesto-api',
          author='Desarrollo DiTeSi, FCE',
          author_email='ditesi@econo.unlp.edu.ar',
          classifiers=[
            #   3 - Alpha
            #   4 - Beta
            #   5 - Production/Stable
            'Development Status :: 3 - Alpha',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.5'
          ],
          packages=find_packages(exclude=['contrib', 'docs', 'test*']),
          install_requires=[
              'psycopg2-binary',
              'sqlalchemy',
              'dateutils',
              'google-api-python-client',
              'google-auth-httplib2',
              'google-auth-oauthlib',
              'oauth2client',
              'Flask',
              'flask-cors',
              'gunicorn',
              'ptvsd',
              'warden-api'
          ],
          entry_points={
#            'console_scripts': [
#                'rest=digesto.api.rest.main:main'
#            ]
          }
      )
