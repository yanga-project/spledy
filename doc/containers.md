# Containers

{#- A container, or an integration component, with its pages by kind, the same on every platform. -#}
{% for component in report_data.components if report_data.files("container", component.name) %}

## {{ component.name }}

{% set pages = namespace(lines=[]) %}
{% for kind in ["docs", "sources", "test", "coverage", "static-analysis"] %}
{% set pages.lines = pages.lines + report_data.files("container", component.name, kind) %}
{% endfor %}
{% set pages.lines = pages.lines + (report_data.files("container", component.name) | reject("in", pages.lines) | list) %}

{% if component.subcomponents %}
Subcomponents: {{ component.subcomponents | join(", ") }}
{% endif %}
{% if component.integrates %}
Integrates: {{ component.integrates | join(", ") }}
{% endif %}

```{toctree}
:maxdepth: 1

{% for file in pages.lines %}
{{ file }}
{% endfor %}
```

{% endfor %}
