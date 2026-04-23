---
layout: default
title: Tars
---
# {{ page.title }}

{{ page.description }}

{% for post in site.posts %}

## [{{ post.title }}]({{ post.url }})

{{ post.date | date: "%B %-d, %Y" }}{% if post.description %} — {{ post.description }}{% endif %}

 {% endfor %}

built with jekyll · hosted on github pages
