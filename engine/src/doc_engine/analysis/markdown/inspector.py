from abc import ABC, abstractmethod
import os
from pathlib import Path

from engine.src.doc_engine.models.inspection import InspectionResult
from engine.src.doc_engine.models.recipe import ComponentConfig


inspection_registry:dict[str, BaseOjbjectInspector] = {}

class MarkdownSource:
    path: Path
    content: str
    lines: list[str]

class BaseOjbjectInspector(ABC):

    @abstractmethod
    def inspect(self, component:ComponentConfig) -> InspectionResult:
        ...

class MarkdownInspector(BaseOjbjectInspector):
    def inspect(self, component:ComponentConfig)  -> InspectionResult:
        '''
        task.format_type = md
        '''
        result = InspectionResult()
        content = self.read_md(component.source)
        # Inspeciona por variáveis e alimenta diagnósticos
        self.discover_variable_references(content, result)
        # Inspeciona por diretivas e alimenta diagnósticos
        self.discover_directives_calls(content, result)
        return result
    
    def read_md(self, path) -> MarkdownSource:
        if not os.path.exists(path):
            return
        
        return MarkdownSource(
            path = Path(path)
        )

        content = read_md(task.source_path)
        task.cache = content

        VariableInspector().inspect(task)
        return super().inspect(task)
    
    def discover_fields(self, component:MarkdownSource, result: InspectionResult):
        if component.type == "template":
            if not os.path.exists(component.source):
                return
                
            metadata, body = self.parser.parse_front_matter(component.source)
            variables = self.parser.extract_variables(body)
            fields_metadata = metadata.get("fields_definition", {})
            
            for var in variables:
                if var not in consolidated_fields:
                    # Fallback definitions if not explicitly typed in YAML front matter
                    consolidated_fields[var] = fields_metadata.get(var, {
                        "data_type": "text",
                        "label": var.replace("_", " ").title(),
                        "source_component": component.id
                    })
        return consolidated_fields


# class VariableInspector(BaseOjbjectInspector):
#     def inspect(self, task:InspectElement) -> list[InspectElement]:
#         if not task.has_cache:
#             content = read_md(task.source_path)
#             task.cache = content
        
#         InspectElement(
#                 id='',
#                 source_path=task.source,
#                 file_format=task.file_format,
#                 content = task.cache
#         )


#         return super().inspect(task)


# class ManifestInspector():
#     def __init__(
#             self,
#             manifest:RecipeManifest,
#             registry:dict[str, BaseOjbjectInspector]
#             ):
#         self.manifest = manifest
#         self.inspection_registry = registry
#         self.elements:list[InspectElement] = []

#     def populate_schedule(self):
#         for component in self.manifest.components:
#             task = InspectElement(
#                 id='',
#                 source_path=component.source,
#                 file_format=component.file_format
#             )
#             self.elements.append(task)

#     def proccess_dependencies(self,
#                 user_input,
#                 id,
#                 content,
#                 tree = {}
#         ):
#         self.populate_schedule()

#         for task in self.elements:
#             inspector = self.inspection_registry.get(task.file_format)
#             inspector.inspect(task)
        
#         return self.elements
        
        
        

