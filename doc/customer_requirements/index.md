# Customer Requirements

What each customer of the product line asks for, one need per requirement. The software requirements
link to the customer requirements they satisfy.

{# A customer requirement belongs to the customer of a variant, so the variant decides, not a feature. #}
{% if report_data.has_spl_scope or report_data.variant_name == "Disco" %}
## Customer A: Disco Light

```{custreq} Blinking light
:id: CR_DISCO-001

While the light is on, it blinks, and the user sets how fast it blinks with the main knob.
```
{% endif %}
