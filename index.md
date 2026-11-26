{% if report_data.has_component_scope %}

# Software Component Report - {{ report_data.component_name }}

**Variant:** {{ report_data.variant_name }}</br>
**Component:** {{ report_data.component_name }}</br>
**Platform:** {{ report_data.platform_name }}</br>
**Timestamp:** {{ env.timestamp }}

{{ report_data.create_component_myst_toc(report_data.component_name) }}

```{toctree}
:maxdepth: 1

/doc/traceability
```

{% elif report_data.has_spl_scope %}

# {{ report_data.project_name }} - Product Line Documentation

**Timestamp:** {{ env.timestamp }}

```{toctree}
:maxdepth: 2
:caption: Contents

/doc/customer_requirements/index
/doc/features/index
/doc/hazard_analysis/index
/doc/software_requirements/index
/doc/software_architecture/index
/doc/trace_model
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
/doc/features/index
/doc/hazard_analysis/index
/doc/software_requirements/index
/doc/software_architecture/index
/doc/components
{% if report_data.files("container") %}
/doc/containers
{% endif %}
/doc/variant_tests/index
{% for file in report_data.files("variant", "configuration") %}
{{ file }}
{% endfor %}
/doc/reports
{% for file in report_data.untagged() %}
{{ file }}
{% endfor %}

```

{% endif %}
