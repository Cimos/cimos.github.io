---
layout: default
title: Tags
permalink: /tags
---

<a href="{{ '/' | relative_url }}">{{ site.theme_config.back_home_text }}</a>
<h1>Tags</h1>

{% assign sorted = site.tags | sort %}

<div class="tag-cloud">
  {% for t in sorted %}
    <a class="tag" href="#{{ t[0] | slugify }}">{{ t[0] }} <span class="tag-count">{{ t[1].size }}</span></a>
  {% endfor %}
</div>

{% for t in sorted %}
  <h2 id="{{ t[0] | slugify }}" class="tag-heading">{{ t[0] }}</h2>
  <ul>
    {% for p in t[1] %}
      <li class="post-list-item">
        <span class="home-date">{{ p.date | date: site.theme_config.date_format }}»</span>
        <a href="{{ p.url | relative_url }}">{{ p.title }}</a>
      </li>
    {% endfor %}
  </ul>
{% endfor %}
