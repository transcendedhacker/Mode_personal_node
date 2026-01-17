# adding custom library

## example: hair color library

your reference: `HairColors.txt`

```
Platinum blonde hair: Blindingly bright, metallic white-blonde...
Icy white hair: Pure, snow-white hair strands with cool blue...
```

convert to:

```json
{
  "meta": {
    "name": "hair_colors",
    "version": "1.0"
  },
  
  "blocks": {
    "color": {
      "Platinum Blonde": "Blindingly bright, metallic white-blonde hair that reflects light",
      "Icy White": "Pure, snow-white hair strands with cool blue undertones",
      "Silver Grey": "Metallic grey hair that looks like spun sterling silver"
    }
  }
}
```

save as `libraries/hair_colors.json`

## notes

- dropdown name = key ("Platinum Blonde")
- description = value (the actual text)
- block name ("color") must match schema order

## schema update

add "color" to assembly order in `schema/connector.json`:

```json
"order": [
  "subject",
  "color",
  "hairstyle",
  ...
]
```

restart comfy.
