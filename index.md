---
layout: default
title: Tars
---
# {{ page.title }}

{{ page.description }}

## Posts

{% for post in site.posts %}

## [{{ post.title }}]({{ post.url | relative_url }})

{{ post.date | date: "%B %-d, %Y" }}{% if post.description %} — {{ post.description }}{% endif %}

{% endfor %}

## Courses

{% assign courses = site.courses | sort: "order" %}
{% for course in courses %}

## [{{ course.title }}]({{ course.url | relative_url }})

{% if course.description %}{{ course.description }}{% endif %}

{% endfor %}

built with jekyll · hosted on github pages
