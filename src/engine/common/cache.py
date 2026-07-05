import os
import hashlib
import json
import logging

logger = logging.getLogger("doc_engine.cache")

class CacheManager:
    """
    Manages asset serialization states using SHA256 hashing to prevent 
    unnecessary re-compilation of heavy external assets.
    """
    def __init__(self, cache_dir: str):
        self.cache_dir = cache_dir
        self.registry_path = os.path.join(cache_dir, "cache_registry.json")
        self.registry = self._load_registry()

    def _load_registry(self) -> dict:
        """Loads the existing cache registry file from disk."""
        if os.path.exists(self.registry_path):
            try:
                with open(self.registry_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Failed to read cache registry, resetting: {e}")
        return {}

    def _save_registry(self):
        """Persists the current cache registry state back to disk."""
        os.makedirs(self.cache_dir, exist_ok=True)
        try:
            with open(self.registry_path, 'w', encoding='utf-8') as f:
                json.dump(self.registry, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save cache registry: {e}")

    @staticmethod
    def calculate_file_hash(file_path: str) -> str:
        """Generates a unique SHA256 checksum string for a given file asset."""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            # Read file in chunks of 4k to prevent RAM spike on massive files
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    @staticmethod
    def calculate_text_hash(text: str) -> str:
        """Generates a unique SHA256 checksum string for raw text strings (e.g., Mermaid blocks)."""
        return hashlib.sha256(text.encode('utf-8')).hexdigest()

    def is_cached(self, asset_id: str, current_hash: str, expected_outputs: list) -> bool:
        """
        Verifies if the asset match recorded hash credentials and checks 
        if all expected physical file outputs actually exist on disk.
        """
        cached_entry = self.registry.get(asset_id)
        if not cached_entry:
            return False
        
        # Check if hash values match perfectly
        if cached_entry.get("hash") != current_hash:
            return False
            
        # Check if files generated in previous run were not deleted
        for file_path in expected_outputs:
            if not os.path.exists(file_path):
                return False
                
        return True

    def update_cache(self, asset_id: str, current_hash: str, outputs: list):
        """Records a new finalized compilation asset fingerprint entry to registry cache."""
        self.registry[asset_id] = {
            "hash": current_hash,
            "updated_at": os.path.getmtime(self.registry_path) if os.path.exists(self.registry_path) else None,
            "outputs": outputs
        }
        self._save_registry()