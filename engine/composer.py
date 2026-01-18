"""
Deterministic prompt assembly engine for diffusion models.

This module implements schema-driven prompt generation with strict separation
between engine logic, structural contracts, and content libraries.
"""

import json
import os
import glob
from typing import Dict, List, Optional, Any


class Composer:
    """
    Schema-driven prompt composer for structured image generation.
    
    Loads a schema contract and content libraries, then assembles prompts
    according to model-specific ordering and weighting constraints.
    """
    
    def __init__(self, schema_path: str, lib_path: str):
        """
        Initialize composer with schema and libraries.
        
        Args:
            schema_path: Path to schema JSON file
            lib_path: Path to directory containing library JSON files
        """
        self.schema = self._load(schema_path)
        self.libs = self._load_libs(lib_path)
        self.cache: Dict[str, List[str]] = {}
        
        # Validate schema version
        if "schema_version" not in self.schema:
            raise ValueError("Schema missing version field")
    
    def _load(self, path: str) -> Dict[str, Any]:
        """Load JSON file."""
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _load_libs(self, path: str) -> Dict[str, Dict[str, Any]]:
        """Load all library JSON files from directory."""
        libs = {}
        for f in glob.glob(os.path.join(path, "*.json")):
            name = os.path.splitext(os.path.basename(f))[0]
            libs[name] = self._load(f)
        return libs
    
    def get_lib_names(self) -> List[str]:
        """Return sorted list of available library names."""
        return sorted(list(self.libs.keys()))
    
    def get_options(self, lib: str, block: str, include_none: bool = True) -> List[str]:
        """
        Get available options for a block in a library.
        
        Args:
            lib: Library name
            block: Block name
            include_none: Whether to prepend "None" option
            
        Returns:
            Sorted list of option names
        """
        key = f"{lib}:{block}"
        if key in self.cache:
            return self.cache[key]
        
        if lib not in self.libs:
            opts = ["None"] if include_none else []
            self.cache[key] = opts
            return opts
        
        blocks = self.libs[lib].get("blocks", {})
        opts = sorted(list(blocks.get(block, {}).keys()))
        
        if include_none:
            opts = ["None"] + opts
        
        self.cache[key] = opts
        return opts
    
    def _apply_weight(self, text: str, weight: float, model: str) -> str:
        """
        Apply weighting syntax to text based on model configuration.
        
        Args:
            text: Text to weight
            weight: Weight multiplier
            model: Target model name
            
        Returns:
            Weighted text string
        """
        cfg = self.schema["models"].get(model, {})
        if not cfg.get("weights", False) or weight == 1.0:
            return text
        
        adjusted_weight = weight * cfg.get("multiplier", 1.0)
        return f"({text}:{adjusted_weight:.1f})"
    
    def compose(
        self, 
        lib: str, 
        selections: Dict[str, str], 
        model: str = "sdxl",
        addons: Optional[Dict[str, str]] = None,
        intent_flags: Optional[Dict[str, str]] = None
    ) -> str:
        """
        Assemble prompt from selections according to schema.
        
        Args:
            lib: Library name to use
            selections: Dictionary of {block_name: selected_option}
            model: Target model ("sdxl" or "flux")
            addons: Optional dictionary of {block_name: addon_text}
            intent_flags: Optional dictionary of {flag_name: flag_value}
            
        Returns:
            Assembled prompt string
        """
        print(f"\n[COMPOSER] compose() called with lib={lib}, model={model}")
        print(f"[COMPOSER] selections={selections}")
        print(f"[COMPOSER] addons={addons}")
        
        lib_data = self.libs.get(lib, {})
        blocks = lib_data.get("blocks", {})
        
        print(f"[COMPOSER] Library has {len(blocks)} blocks")
        
        if addons is None:
            addons = {}
        if intent_flags is None:
            intent_flags = {}
        
        # Apply default intent flags
        for flag_name, flag_config in self.schema.get("intent_flags", {}).items():
            if flag_name not in intent_flags:
                intent_flags[flag_name] = flag_config["default"]
        
        asm = self.schema["assembly"]
        weights = self.schema.get("weights", {})
        
        parts = []
        order = asm["order"]
        sep = asm["separator"]
        breaks = asm.get("break_after", [])
        
        for i, block in enumerate(order):
            # Get selection or skip
            sel = selections.get(block)
            print(f"[COMPOSER] Block {i}: {block} -> selection='{sel}'")
            
            if not sel or sel == "None":
                print(f"[COMPOSER]   Skipped (None or empty)")
                continue
            
            # Get text from library
            text = blocks.get(block, {}).get(sel, "")
            print(f"[COMPOSER]   Library text: '{text}'")
            
            if not text:
                print(f"[COMPOSER]   Skipped (no text in library)")
                continue
            
            # Merge addon if present
            block_config = self.schema.get("blocks", {}).get(block, {})
            if block_config.get("addon_enabled", False) and block in addons:
                addon = addons[block].strip()
                if addon:
                    merge_mode = block_config.get("addon_merge_mode", "inline_append")
                    if merge_mode == "inline_append":
                        text = f"{text}, {addon}"
                    print(f"[COMPOSER]   Added addon: '{addon}' -> new text: '{text}'")
            
            # Apply weighting
            w = weights.get(block, 1.0)
            weighted_text = self._apply_weight(text, w, model)
            print(f"[COMPOSER]   Weight: {w} -> '{weighted_text}'")
            parts.append(weighted_text)
            
            # Insert BREAK tokens at specified positions
            if (i + 1) in breaks:
                parts.append("BREAK")
                print(f"[COMPOSER]   Added BREAK after position {i+1}")
        
        # Add provenance comment if enabled
        provenance_config = self.schema.get("provenance", {})
        if provenance_config.get("enabled", False):
            comment = provenance_config.get("comment", "")
            if comment:
                parts.insert(0, comment)
        
        final_prompt = sep.join(parts)
        print(f"[COMPOSER] Final assembled prompt: '{final_prompt}'")
        print(f"[COMPOSER] ===END===\n")
        
        return final_prompt
    
    def validate_selection(self, lib: str, block: str, option: str) -> bool:
        """
        Validate that an option exists in a library block.
        
        Args:
            lib: Library name
            block: Block name
            option: Option name
            
        Returns:
            True if option exists, False otherwise
        """
        if lib not in self.libs:
            return False
        
        blocks = self.libs[lib].get("blocks", {})
        if block not in blocks:
            return False
        
        return option in blocks[block]
