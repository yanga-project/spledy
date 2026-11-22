{% if report_data.has_component_scope %}

# Software Component Report - {{ report_data.component_name }}

**Variant:** {{ report_data.variant_name }}</br>
**Component:** {{ report_data.component_name }}</br>
**Platform:** {{ report_data.platform_name }}</br>
**Timestamp:** {{ env.timestamp }}

{{ report_data.create_component_myst_toc(report_data.component_name) }}

{% elif report_data.has_spl_scope %}

# {{ report_data.project_name }} - Product Line Documentation

**Timestamp:** {{ env.timestamp }}

```{toctree}
:maxdepth: 2
:caption: Contents

/doc/customer_requirements/index
/doc/software_architecture/index
/doc/platforms/index
```

{% else %}

# Variant Report

**Variant:** {{ report_data.variant_name }}</br>
**Platform:** {{ report_data.platform_name }}</br>
**Timestamp:** {{ env.timestamp }}


```{toctree}
:maxdepth: 3
:caption: Contents

/doc/customer_requirements/index
/doc/software_architecture/index
/doc/components
{% if report_data.files("container") %}
/doc/containers
{% endif %}
{% for file in report_data.files("variant", "configuration") %}
{{ file }}
{% endfor %}
{% if report_data.files("merged") or report_data.files("variant", "test") or report_data.files("variant", "coverage") or report_data.files("overall") %}
/doc/reports
{% endif %}
{% for file in report_data.untagged() %}
{{ file }}
{% endfor %}

```

{% endif %}
