# Projects

Here are my featured projects.

<div class="project-grid">
{% for project in list_pinned_projects() %}
  <a href="{{ project.url }}" class="project-card-link">
    <div class="project-card">
      <div class="project-card-content">
        <h3>{{ project.title }}</h3>
        <div class="tag-container">
                {% for tag in project.tags %}
                    <span class="tag-pill">{{ tag }}</span>
                {% endfor %}
        </div>
        <p>{{ project.description }}</p>
      </div>
    </div>
  </a>
{% endfor %}
</div>