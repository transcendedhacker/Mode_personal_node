# notes

## structure

atomic parts in libs → schema defines assembly → engine composes

no bloat in dropdowns. each option = one thing.

## adding libs

1. drop json in libraries/
2. match block names in schema order
3. restart comfy

## schema tweaks

weights in connector.json apply to all libs.
break positions = where to insert BREAK.

## model profiles

sdxl: weight_multiplier 1.0
flux: weight_multiplier 0.85 (lighter)

## todo

- [ ] add more hair options from reference
- [ ] parse outfit list properly
- [ ] atmosphere lib needs work
- [ ] maybe add location block

## perf notes

gen time should be <100s with clean prompts.
if slow, check for malformed output or clip issues.

old system was hitting 300s - too much crap in prompt.
