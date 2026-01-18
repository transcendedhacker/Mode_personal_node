"""
Mode_personal_node: Schema-driven prompt generation engine for ComfyUI.

Licensed under CC BY-NC 4.0.
"""

import os
import sys

node_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, node_path)

from engine.composer import Composer

SCHEMA = os.path.join(node_path, "schema", "connector.json")
LIBS = os.path.join(node_path, "libraries")


class PromptComposerNode:
    """
    Structured prompt composition node for diffusion models.
    
    Provides dropdown-based selection interface for schema-defined blocks,
    assembling prompts according to model-specific ordering constraints.
    Each block supports an optional addon string for inline modification.
    """
    
    def __init__(self):
        self.composer = Composer(SCHEMA, LIBS)
    
    @classmethod
    def INPUT_TYPES(cls):
        """Define node input structure."""
        inst = cls()
        c = inst.composer
        
        libs = c.get_lib_names()
        if not libs:
            libs = ["default"]
        
        default_lib = libs[0]
        order = c.schema["assembly"]["order"]
        
        # Start with base inputs
        inputs = {
            "required": {},
            "optional": {}
        }
        
        # Add library and model first
        inputs["required"]["library"] = (libs,)
        inputs["required"]["model"] = (["sdxl", "flux"], {"default": "sdxl"})
        
        # Add each block dropdown (NO addons yet - we'll add them after)
        for block in order:
            opts = c.get_options(default_lib, block, include_none=True)
            inputs["required"][block] = (opts,)
        
        # Now add ALL addons as optional at the end
        for block in order:
            addon_key = f"{block}_addon"
            inputs["optional"][addon_key] = ("STRING", {
                "default": "",
                "multiline": False
            })
        
        # Add global custom text input
        inputs["optional"]["custom"] = ("STRING", {
            "multiline": True,
            "default": ""
        })
        
        return inputs
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt",)
    FUNCTION = "compose_prompt"
    CATEGORY = "prompting/structured"
    
    def compose_prompt(self, library, model, custom="", **kwargs):
        """
        Compose prompt from selections and addons.
        
        Args:
            library: Selected library name
            model: Target model (sdxl/flux)
            custom: Optional custom text to append
            **kwargs: Block selections and addon strings
            
        Returns:
            Tuple containing assembled prompt string
        """
        # DEBUG: Print all received arguments
        print("\n=== DEBUG: compose_prompt called ===")
        print(f"Library: {library}")
        print(f"Model: {model}")
        print(f"Custom: {custom}")
        print(f"All kwargs keys: {list(kwargs.keys())}")
        print(f"All kwargs: {kwargs}")
        
        order = self.composer.schema["assembly"]["order"]
        
        # Separate selections from addons
        selections = {}
        addons = {}
        
        for key, value in kwargs.items():
            if key.endswith("_addon"):
                # This is an addon string
                block_name = key.replace("_addon", "")
                if value and value.strip():
                    addons[block_name] = value.strip()
                    print(f"Addon: {block_name} = '{value.strip()}'")
            else:
                # This is a block selection
                if value and value != "None":
                    selections[key] = value
                    print(f"Selection: {key} = '{value}'")
        
        print(f"\nFinal selections: {selections}")
        print(f"Final addons: {addons}")
        
        # Assemble prompt with addons
        prompt = self.composer.compose(library, selections, model, addons=addons)
        
        print(f"\nGenerated prompt: {prompt}")
        print("=== END DEBUG ===\n")
        
        # Append global custom text if provided
        if custom.strip():
            prompt += ", BREAK, " + custom.strip()
        
        return (prompt,)


class NegativePromptNode:
    """
    Configurable negative prompt generator.
    
    Provides boolean toggles for common negative prompt categories,
    with optional custom text addition.
    """
    
    CATEGORIES = {
        "quality": "blurry, low quality, jpeg artifacts, watermark, signature",
        "anatomy": "deformed face, asymmetrical eyes, bad proportions, extra limbs, merged fingers",
        "style": "cartoon, anime, 3d render, illustration, artificial",
        "lighting": "harsh shadows, overexposed, underexposed, bad lighting",
        "context": "multiple people, cluttered background, busy composition",
        "texture": "duplicate, pixelated, grainy noise, compression artifacts"
    }
    
    @classmethod
    def INPUT_TYPES(cls):
        """Define node input structure."""
        return {
            "required": {
                "quality": ("BOOLEAN", {"default": True}),
                "anatomy": ("BOOLEAN", {"default": True}),
                "style": ("BOOLEAN", {"default": True}),
                "lighting": ("BOOLEAN", {"default": False}),
                "context": ("BOOLEAN", {"default": False}),
                "texture": ("BOOLEAN", {"default": True}),
            },
            "optional": {
                "custom": ("STRING", {"multiline": True, "default": ""})
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("negative",)
    FUNCTION = "compose_negative"
    CATEGORY = "prompting/structured"
    
    def compose_negative(self, quality, anatomy, style, lighting, context, texture, custom=""):
        """
        Compose negative prompt from selected categories.
        
        Args:
            quality: Include quality-related negatives
            anatomy: Include anatomy-related negatives
            style: Include style-related negatives
            lighting: Include lighting-related negatives
            context: Include context-related negatives
            texture: Include texture-related negatives
            custom: Optional custom negative text
            
        Returns:
            Tuple containing assembled negative prompt string
        """
        parts = []
        
        if quality:
            parts.append(self.CATEGORIES["quality"])
        if anatomy:
            parts.append(self.CATEGORIES["anatomy"])
        if style:
            parts.append(self.CATEGORIES["style"])
        if lighting:
            parts.append(self.CATEGORIES["lighting"])
        if context:
            parts.append(self.CATEGORIES["context"])
        if texture:
            parts.append(self.CATEGORIES["texture"])
        
        if custom.strip():
            parts.append(custom.strip())
        
        return (", ".join(parts),)


# ComfyUI node registration
NODE_CLASS_MAPPINGS = {
    "PromptComposerNode": PromptComposerNode,
    "NegativePromptNode": NegativePromptNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PromptComposerNode": "Structured Prompt Composer",
    "NegativePromptNode": "Structured Negative Prompt"
}
