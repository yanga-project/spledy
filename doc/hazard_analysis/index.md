# Hazard Analysis

The hazards the functions of the product line can bring, each with the function (software
requirement) it arises from and the safety goal that mitigates it.

{% if report_data.has_spl_scope or report_data.features.BLINKING %}
```{hazard} Flashing light triggers a photosensitive seizure
:id: HAZ_BLINK-001
:arises_from: SWRS_BLINK-001

A light that flashes fast can trigger a seizure in a person with photosensitive epilepsy. Only a
variant that blinks has this hazard.
```

```{safetygoal} At most three flashes in any one second
:id: SG_BLINK-001
:mitigates: HAZ_BLINK-001

The light flashes no more than three times in any one-second period. A flash is a pair of opposing
changes: the light goes on and off.

The limit is the one of WCAG 2.2, success criterion 2.3.1 "Three Flashes or Below Threshold"
(<https://www.w3.org/TR/WCAG22/#three-flashes-or-below-threshold>). That guideline is written for
content on a screen; applying it to a lamp is our own choice. We use the flash count only, without
the area threshold the guideline also allows, which is the stricter reading.
```
{% endif %}
