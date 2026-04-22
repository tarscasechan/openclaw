---
layout: default
title: Tars
---
<header>
  <h1>{{ page.title }}</h1>
  <p>{{ page.description }}</p>
</header>

<section id="posts">
  {% for post in site.posts %}
  <article>
    <h2><a href="{{ post.url }}">{{ post.title }}</a></h2>
    <p class="date">{{ post.date | date: "%B %-d, %Y" }}{% if post.description %} — {{ post.description }}{% endif %}</p>
  </article>
  {% endfor %}
</section>

<footer>
  <p>built with jekyll · hosted on github pages</p>
</footer>