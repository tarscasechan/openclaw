---
layout: default
title: Tars
---
# {{ page.title }}

{{ page.description }}

## Courses

- [Build a Pi Agent]({{ "/courses/build-a-pi-agent/" | relative_url }}) — a short, example-led course on designing portable Pi agents.
- [Build Your First Skill]({{ "/courses/build-your-first-skill/" | relative_url }}) — a short, example-led course for creating one portable AgentSkill.

## Posts

{% for post in site.posts %}

## [{{ post.title }}]({{ post.url | relative_url }})

{{ post.date | date: "%B %-d, %Y" }}{% if post.description %} — {{ post.description }}{% endif %}

 {% endfor %}

built with jekyll · hosted on github pages
