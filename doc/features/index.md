# Features

The features of the feature model, one need per feature. The feature model is built from the customer
requirements: it holds a feature only where customers differ, so that a function can be switched on or
off or set per variant. A feature has no trace links; each need names its definition in the feature
model (`KConfig`).

{% if report_data.has_spl_scope or report_data.features.BLINKING %}
```{feature} Blinking
:id: FEAT_BLINKING

Switches the blinking function on: Disco blinks, Sleep and Spa do not. Defined as
[`config BLINKING`](source:KConfig#2) in the feature model.
```
{% endif %}
