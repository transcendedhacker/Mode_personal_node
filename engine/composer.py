import json
import os
import glob

class Composer:
    def __init__(self, schema_path, lib_path):
        self.schema = self._load(schema_path)
        self.libs = self._load_libs(lib_path)
    
    def _load(self, path):
        with open(path, 'r') as f:
            return json.load(f)
    
    def _load_libs(self, path):
        libs = {}
        for f in glob.glob(os.path.join(path, "*.json")):
            name = os.path.splitext(os.path.basename(f))[0]
            libs[name] = self._load(f)
        return libs
    
    def get_lib_names(self):
        return list(self.libs.keys())
    
    def get_options(self, lib, block):
        if lib not in self.libs:
            return []
        blocks = self.libs[lib].get("blocks", {})
        return list(blocks.get(block, {}).keys())
    
    def _weight(self, text, w, model):
        cfg = self.schema["models"].get(model, {})
        if not cfg.get("weights", False) or w == 1.0:
            return text
        aw = w * cfg.get("multiplier", 1.0)
        return f"({text}:{aw:.1f})"
    
    def compose(self, lib, selections, model="sdxl"):
        lib_data = self.libs.get(lib, {})
        blocks = lib_data.get("blocks", {})
        
        asm = self.schema["assembly"]
        weights = self.schema["weights"]
        
        parts = []
        order = asm["order"]
        sep = asm["separator"]
        breaks = asm.get("break_after", [])
        
        for i, block in enumerate(order):
            sel = selections.get(block)
            if not sel:
                continue
            
            text = blocks.get(block, {}).get(sel, "")
            if not text:
                continue
            
            w = weights.get(block, 1.0)
            parts.append(self._weight(text, w, model))
            
            if (i + 1) in breaks:
                parts.append("BREAK")
        
        return sep.join(parts)
