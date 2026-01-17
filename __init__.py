import os
import sys

node_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, node_path)

from engine.composer import Composer

SCHEMA = os.path.join(node_path, "schema", "connector.json")
LIBS = os.path.join(node_path, "libraries")

class PromptNode:
    def __init__(self):
        self.c = Composer(SCHEMA, LIBS)
    
    @classmethod
    def INPUT_TYPES(cls):
        inst = cls()
        c = inst.c
        
        libs = c.get_lib_names()
        if not libs:
            libs = ["default"]
        
        default_lib = libs[0]
        order = c.schema["assembly"]["order"]
        
        inputs = {"required": {"library": (libs,), "model": (["sdxl", "flux"], {"default": "sdxl"})}}
        
        for block in order:
            opts = c.get_options(default_lib, block, include_none=True)
            inputs["required"][block] = (opts,)
        
        inputs["optional"] = {"custom": ("STRING", {"multiline": True, "default": ""})}
        
        return inputs
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt",)
    FUNCTION = "run"
    CATEGORY = "Modular Prompts"
    
    def run(self, library, model, custom="", **kwargs):
        sels = {k: v for k, v in kwargs.items() if v != "None"}
        prompt = self.c.compose(library, sels, model)
        
        if custom.strip():
            prompt += ", BREAK, " + custom.strip()
        
        return (prompt,)


class NegativeNode:
    NEGS = {
        "q": "blurry, low quality, jpeg artifacts, watermark, signature",
        "a": "deformed face, asymmetrical eyes, bad proportions, extra limbs, merged fingers",
        "s": "cartoon, anime, 3d render, illustration, artificial",
        "l": "harsh shadows, overexposed, underexposed, bad lighting",
        "c": "multiple people, cluttered background, busy composition",
        "t": "duplicate, pixelated, grainy noise, compression artifacts"
    }
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "quality": ("BOOLEAN", {"default": True}),
                "anatomy": ("BOOLEAN", {"default": True}),
                "style": ("BOOLEAN", {"default": True}),
                "lighting": ("BOOLEAN", {"default": False}),
                "context": ("BOOLEAN", {"default": False}),
                "texture": ("BOOLEAN", {"default": True}),
            },
            "optional": {"custom": ("STRING", {"multiline": True, "default": ""})}
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("negative",)
    FUNCTION = "run"
    CATEGORY = "Modular Prompts"
    
    def run(self, quality, anatomy, style, lighting, context, texture, custom=""):
        parts = []
        if quality: parts.append(self.NEGS["q"])
        if anatomy: parts.append(self.NEGS["a"])
        if style: parts.append(self.NEGS["s"])
        if lighting: parts.append(self.NEGS["l"])
        if context: parts.append(self.NEGS["c"])
        if texture: parts.append(self.NEGS["t"])
        if custom.strip(): parts.append(custom.strip())
        
        return (", ".join(parts),)


NODE_CLASS_MAPPINGS = {"PromptNode": PromptNode, "NegativeNode": NegativeNode}
NODE_DISPLAY_NAME_MAPPINGS = {"PromptNode": "Prompt Composer", "NegativeNode": "Negative Prompt"}
