# Software Requirements

The requirements on the software of the product line. A functional requirement satisfies a customer
requirement, a safety requirement satisfies a safety goal. The condition of a feature decides which
variants have the requirements of a function.

{% if report_data.has_spl_scope or report_data.features.BLINKING %}
% Gap on purpose: SWRS_BLINK-001 has no variant test, so the Traceability Report page shows a `req-is-tested`
% finding for it. Do not add a test to remove the finding.

```{req} Blink period follows the main knob
:id: SWRS_BLINK-001
:satisfies: CR_DISCO-001

While the light is on, it switches between on and off. The higher the main knob value, the shorter
the time between two switches.
```

```{req} The light switches no faster than every 170 ms
:id: SWRS_BLINK-002
:satisfies: SG_BLINK-001

The time between two switches of the light is at least 170 ms. The light then flashes at most
2.9 times in one second (1000 ms divided by two switches of 170 ms each).
```
{% endif %}
