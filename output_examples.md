# test output examples

## example 1: minimal selections

**selections:**
- library: comprehensive_portrait
- model: sdxl
- subject: Woman
- hair_color: Platinum Blonde
- outfit: Silk Slip Dress
- all others: None

**output:**
```
A woman with platinum blonde hair, wearing red silk slip dress with spaghetti straps, 
photorealistic, sharp focus, highly detailed, 8k
```

clean. no bloat.

---

## example 2: full composition

**selections:**
- subject: Young Woman
- age: 23-27
- hair_color: Auburn
- hair_style: Long Straight Cascading
- hair_ornament: Silk Bow
- outfit: Black Velvet Mini
- outfit_detail: Glossy Finish
- pose: Over Shoulder
- mood: Dramatic Noir
- location: City Street
- location_detail: Neon-Lit Night
- atmosphere: Neon Pink Teal
- lighting: Neon Reflections
- angle: Eye-Level
- frame: Shallow DOF
- filter: Cyberpunk Neon
- technical: 85mm Portrait

**output:**
```
A young woman 23-27 years old with auburn hair long silky straight hair cascading down the back 
with large decorative silk bow, wearing black velvet mini dress with long sleeves with glossy finish, 
(turning back to camera, looking over shoulder:1.2), (dramatic noir, hard-boiled mystery:1.2), 
on rain-soaked city street during neon-lit midnight, BREAK, 
(saturated neon pink lighting with deep teal shadows:1.3), 
(neon light reflections, colorful urban glow:1.3), eye-level shot, shallow depth of field, soft bokeh background, 
BREAK, cyberpunk neon with crushed blacks, shot on 85mm lens, f/1.8, compressed perspective
```

full composition. weighted. BREAK placement. clean structure.

---

## example 3: skip categories strategically

**selections:**
- subject: Woman
- age: None
- hair_color: Silver Grey
- hair_style: Short Tousled
- hair_ornament: None
- outfit: Leather Jacket
- outfit_detail: None
- pose: Hands On Hips
- mood: Gritty Realism
- location: Industrial Loft
- location_detail: None
- atmosphere: Cold Metallic Grey
- lighting: Side Key Light
- angle: Low Angle
- frame: None
- filter: None
- technical: SDXL Cinematic

**output:**
```
A woman with silver-grey hair short tousled curls, wearing black leather motorcycle jacket over band t-shirt, 
(standing with hands on hips, elbows forward:1.2), (gritty realism, street truth:1.2), 
in industrial loft space, BREAK, (cold metallic grey lighting with crystalline reflections:1.3), 
(single key light from side, deep shadows:1.3), low angle shot, BREAK, 
cinematic photography, professional lighting, sharp focus
```

"None" selections = skipped cleanly. no blank text, just omitted.

---

## composition logic

1. collect all non-"None" selections
2. lookup text from library
3. apply weights per schema
4. join with separator
5. insert BREAK at positions
6. done

atomic → weighted → composed.

---

## scaling test

with 100 options per category:

17 categories × 100 options = 1700 total selections

still works. alphabetical makes it scannable.

with 1000 options total across all categories:

still fast. just more dropdown scrolling.

alphabetical + ctrl+f in dropdown = easy navigation.

---

## performance

v1 (full sentences): 300s gen time
v2 (atomic clean): <100s gen time

clean prompts = faster encoding = better results.
