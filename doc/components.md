# Components

{#- One heading per folder of the component paths, so the components show as a folder tree. -#}
{% set tree = namespace(folders=[]) %}
{% for component in report_data.components | rejectattr("subcomponents") | sort(attribute="path") %}
{% set folders = component.path.split("/")[:-1] if component.path else [] %}
{% for folder in folders %}
{% if tree.folders[:loop.index] != folders[:loop.index] %}

{{ "#" * (loop.index + 1) }} {{ folder }}

{% endif %}
{% endfor %}
{% set tree.folders = folders %}

{{ "#" * (folders | length + 2) }} {{ component.name }}


```{toctree}
:maxdepth: 1

{% for file in report_data.get_component_files_list(component.name) %}
{{ file }}
{% endfor %}

```


{% endfor %}
{% set containers = report_data.components | selectattr("subcomponents") | list %}
{% if containers %}

## Containers

{% for container in containers %}
- **{{ container.name }}**: {{ container.subcomponents | join(", ") }}
{% endfor %}
{% endif %}
