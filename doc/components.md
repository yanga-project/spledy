# Components

{#- One heading per folder of the component paths, so the components show as a folder tree. -#}
{% set tree = namespace(folders=[]) %}
{#- Each component's pages by kind, the same on every platform. -#}
{% for component in report_data.components | sort(attribute="path") if report_data.files("component", component.name) %}
{% set folders = component.path.split("/")[:-1] if component.path else [] %}
{% for folder in folders %}
{% if tree.folders[:loop.index] != folders[:loop.index] %}

{{ "#" * (loop.index + 1) }} {{ folder }}

{% endif %}
{% endfor %}
{% set tree.folders = folders %}

{{ "#" * (folders | length + 2) }} {{ component.name }}

{% set pages = namespace(lines=[]) %}
{% for kind in ["docs", "sources", "test", "coverage", "static-analysis"] %}
{% set pages.lines = pages.lines + report_data.files("component", component.name, kind) %}
{% endfor %}
{% set pages.lines = pages.lines + (report_data.files("component", component.name) | reject("in", pages.lines) | list) %}


```{toctree}
:maxdepth: 1

{% for file in pages.lines %}
{{ file }}
{% endfor %}

```


{% endfor %}
