# dev notes

## v2.0 - massive scale

comprehensive library with 300+ atomic options across 17 categories.

## structure

atomic selections → alphabetically sorted dropdowns → "None" skips blocks → composed output

## categories

subject → age → hair_color → hair_style → hair_ornament → outfit → outfit_detail → pose → mood → location → location_detail → atmosphere → lighting → angle → frame → filter → technical

## "None" behavior

selecting "None" in any dropdown = blank/skip that block entirely.

prompt only includes selected options.

## alphabetical sorting

all dropdowns auto-sorted alphabetically (except "None" which stays on top).

makes options easy to find without search.

## scaling

current: 300+ options
can scale to 1000+ by adding more libs

each lib is independent, composer handles all.

## perf

clean atomic composition should keep gen <100s.

if slow: check for malformed prompts or excessive BREAK tokens.

## todo

- add more angles from AngleShot.txt (100+ options)
- expand outfits from Outfits.txt + RevealingOutfit.txt
- add all poses from SexyPoses.txt
- parse LocationsIndoor.txt for location block
- add all atmosphere variations
- all filters from Filters.txt
- lighting effects from full frame light effect.txt

## hierarchical dependency (future)

comfyui limitation: dropdowns can't dynamically change based on other selections.

workaround: use comprehensive libs that cover all combos.

or: create specialized libs (portrait_casual, portrait_formal, etc) and switch library.
