=======
6Spider
=======

[![Circle CI](https://circleci.com/gh/liyy7/6spider.svg?style=svg)](https://circleci.com/gh/liyy7/6spider)
[![Coverage Status](https://coveralls.io/repos/liyy7/6spider/badge.svg?branch=master&service=github)](https://coveralls.io/github/liyy7/6spider?branch=master)

Overview
========

6Spider is a python based crawler, used to crawl specified job postings from job posting sites.

Requirements
============

* Python 2.7.9

Install
=======

* create a virtual python environment

  `pip install virtualenv`
  
  `python -m virtualenv .virtualenv`

* install dependencies

  `pip install -r requirements.txt`

* test

  `py.test ./tests`

* execute

  `scrapy crawl weban`
