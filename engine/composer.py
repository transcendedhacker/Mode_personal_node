"""
Pure composition engine - content agnostic
"""
import json
import os
import glob

class PromptComposer:
    """
    Generic prompt composition engine.
    Knows nothing about content, only follows schema rules.
    """
    
    def __init__(self, schema_path, libraries_path):
        self.schema = self._load_json(schema_path)
        self.libraries = self._load_libraries(libraries_path)
        
    def _load_json(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _load_libraries(self, path):
        libraries = {}
        for json_file in glob.glob(os.path.join(path, "*.json")):
            lib_id = os.path.splitext(os.path.basename(json_file))[0]
            libraries[lib_id] = self._load_json(json_file)
        return libraries
    
    def get_library_names(self):
        return list(self.libraries.keys())
    
    def get_block_options(self, library_id, block_name):
        if library_id not in self.libraries:
            return []
        blocks = self.libraries[library_id].get("blocks", {})
        return list(blocks.get(block_name, {}).keys())
    
    def apply_weight(self, text, weight, model_profile):
        model_config = self.schema["models"].get(model_profile, {})
        if not model_config.get("enable_weights", False):
            return text
        if weight == 1.0:
            return text
        
        adjusted_weight = weight * model_config.get("weight_multiplier", 1.0)
        weight_format = model_config.get("weight_format", "({text}:{weight})")
        
        return weight_format.format(text=text, weight=f"{adjusted_weight:.1f}")
    
    def compose(self, library_id, selections, model_profile="sdxl"):
        """
        Compose final prompt from selections.
        
        Args:
            library_id: Selected library
            selections: Dict of {block_name: selected_option}
            model_profile: "sdxl" or "flux"
        
        Returns:
            Final composed prompt string
        """
        library = self.libraries.get(library_id, {})
        blocks = library.get("blocks", {})
        
        structure = self.schema["structure"]
        weights = self.schema["weights"]
        
        parts = []
        block_order = structure["block_order"]
        separator = structure["separator"]
        break_positions = structure.get("break_positions", [])
        
        for i, block_name in enumerate(block_order):
            selected_option = selections.get(block_name)
            if not selected_option:
                continue
            
            block_data = blocks.get(block_name, {})
            text = block_data.get(selected_option, "")
            
            if not text:
                continue
            
            weight = weights.get(block_name, 1.0)
            weighted_text = self.apply_weight(text, weight, model_profile)
            
            parts.append(weighted_text)
            
            if (i + 1) in break_positions:
                parts.append("BREAK")
        
        return separator.join(parts)
