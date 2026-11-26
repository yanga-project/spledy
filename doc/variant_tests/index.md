# Variant Test Specification

The tests of a whole variant, each with the software requirement it tests and its results.

{% if report_data.features.BLINKING %}
```{vtest} variants.Disco.test_disco_variant.test_blinking_flashes_at_most_three_times_per_second
:id: VT_DISCO-001
:tests: SWRS_BLINK-002

With the knob at 100 (the fastest blink), the light changes at most six times in 100 task cycles of
10 ms, so it flashes at most three times in one second.
```
{% endif %}
