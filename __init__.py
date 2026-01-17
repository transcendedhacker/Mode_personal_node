"""
ComfyUI Node - Minimal interface to composition engine
"""
import os
import sys

node_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, node_path)

from engine.composer import PromptComposer

SCHEMA_PATH = os.path.join(node_path, "schema", "connector.json")
LIBRARIES_PATH = os.path.join(node_path, "libraries")

class ModularPromptNode:
    
    def __init__(self):
        self.composer = PromptComposer(SCHEMA_PATH, LIBRARIES_PATH)
    
    @classmethod
    def INPUT_TYPES(cls):
        instance = cls()
        composer = instance.composer
        
        library_names = composer.get_library_names()
        if not library_names:
            library_names = ["default"]
        
        default_library = library_names[0]
        
        block_order = composer.schema["structure"]["block_order"]
        
        inputs = {
            "required": {
                "library": (library_names,),
                "model_profile": (["sdxl", "flux"], {"default": "sdxl"}),
            }
        }
        
        for block_name in block_order:
            options = composer.get_block_options(default_library, block_name)
            if not options:
                options = ["None"]
            inputs["required"][block_name] = (options,)
        
        inputs["optional"] = {
            "custom_addition": ("STRING", {"multiline": True, "default": ""}),
        }
        
        return inputs
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt",)
    FUNCTION = "compose_prompt"
    CATEGORY = "Modular Prompts"
    
    def compose_prompt(self, library, model_profile, custom_addition="", **kwargs):
        """
        Compose final prompt using engine
        """
        selections = {k: v for k, v in kwargs.items() if v != "None"}
        
        prompt = self.composer.compose(library, selections, model_profile)
        
        if custom_addition.strip():
            prompt += ", BREAK, " + custom_addition.strip()
        
        return (prompt,)


class ModularNegativeNode:
    
    NEGATIVES = {
        "quality": "blurry, out of focus, low quality, jpeg artifacts, watermark, signature",
        "anatomy": "deformed face, asymmetrical eyes, bad proportions, extra limbs, merged fingers",
        "style": "cartoon, anime, 3d render, illustration, painting, artificial",
    }
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "quality": ("BOOLEAN", {"default": True}),
                "anatomy": ("BOOLEAN", {"default": True}),
                "style": ("BOOLEAN", {"default": True}),
            },
            "optional": {
                "custom": ("STRING", {"multiline": True, "default": ""}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("negative",)
    FUNCTION = "compose_negative"
    CATEGORY = "Modular Prompts"
    
    def compose_negative(self, quality, anatomy, style, custom=""):
        parts = []
        if quality:
            parts.append(self.NEGATIVES["quality"])
        if anatomy:
            parts.append(self.NEGATIVES["anatomy"])
        if style:
            parts.append(self.NEGATIVES["style"])
        if custom.strip():
            parts.append(custom.strip())
        
        return (", ".join(parts),)


NODE_CLASS_MAPPINGS = {
    "ModularPromptNode": ModularPromptNode,
    "ModularNegativeNode": ModularNegativeNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ModularPromptNode": "Modular Prompt Composer",
    "ModularNegativeNode": "Modular Negative Prompt",
}
