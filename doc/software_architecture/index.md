# Software Architecture

The architecture follows the arc42 template. This chapter holds section 5, the building block view,
for the elements the requirements so far need; the other sections follow.

## 5 Building Block View

### Level 1

All software components communicate only through the RTE (Runtime Environment). The architecture
elements below realise the software requirements; the detailed design of each component refines
them.

{% if report_data.has_spl_scope or report_data.features.BLINKING %}
```{arch} light_controller
:id: ARCH_LC
:realises: SWRS_BLINK-001, SWRS_BLINK-002

The component that switches the light on and off from the power state and, in a blinking variant,
blinks it.
```
{% else %}
```{arch} light_controller
:id: ARCH_LC

The component that switches the light on and off from the power state.
```
{% endif %}

{% if report_data.has_spl_scope or report_data.features.BLINKING %}
```{arch} RteGetMainKnobValue
:id: ARCH_RTE_MAIN_KNOB
:realises: SWRS_BLINK-001

The RTE interface from which `light_controller` reads the main knob value that sets the blink
period.
```
{% endif %}
