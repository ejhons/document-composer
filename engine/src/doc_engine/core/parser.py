import re
import yaml
from typing import Dict, Set, Any, Tuple

class DocumentParser:
    @staticmethod
    def parse_front_matter(file_path: str) -> Tuple[Dict[str, Any], str]:
        """Extracts YAML front matter and the raw Markdown body from a component file."""
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Match YAML block bounded by --- at the start of the file
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', content, re.DOTALL)
        if match:
            front_matter_text, body_content = match.groups()
            metadata = yaml.safe_load(front_matter_text) or {}
            return metadata, body_content
        
        return {}, content

    @staticmethod
    def extract_variables(content: str) -> Set[str]:
        """Scans raw text to discover all Jinja2 placeholders like {{ variable_name }}."""
        found_tokens = re.findall(r'\{\{\s*([a-zA-Z0-9_]+)\s*\}\}', content)
        return set(found_tokens)