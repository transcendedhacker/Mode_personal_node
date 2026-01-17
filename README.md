# modular prompt composer v2

massive scalable sdxl/flux prompt system with 300+ atomic options.

## features

- 17 categories (subject, age, hair, outfit, pose, mood, location, lighting, angle, filter, etc)
- 300+ options, alphabetically sorted
- "None" option skips blocks
- clean composition, no bloat
- infinitely scalable

## structure

```
engine/     → composition logic
schema/     → assembly rules  
libraries/  → atomic options (sorted, massive)
```

## install

drop in `ComfyUI/custom_nodes/`, restart.

## usage

1. pick library
2. select from dropdowns (or "None" to skip)
3. get composed prompt

atomic parts → clean output.

## scaling

current: 300+ options
can add 1000s more by expanding libs.

each option = one thing. no sentences in dropdowns.

alphabetical sorting + "None" option = easy navigation.
