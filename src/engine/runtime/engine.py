import os
import json
import logging
from jinja2 import Template
from typing import Dict, Any, List
from engine.backend.compilers.registry import CompilerRegistry
from engine.frontend.inspection_pipeline import InspectionPipeline
from engine.planner.graph.dependency_queue import PendingCollector
from engine.planner.graph.dependency_resolver import DependencyResolver
from engine.planner.graph.graph import RecipeGraph
from engine.planner.graph.runtime_resolver import RuntimeResolver
from engine.planner.planning_context import PlanningContext
from engine.runtime.context import ExecutionContext
from engine.runtime.execution_plan import ExecutionPlan
from engine.common.cache import CacheManager
from engine.frontend.parser import MarkdownParser
from engine.planner.manifests.sanitizers import Sanitizers
from engine.backend.adapters.implementations.docx_adapter import DocxPostCompileAdapter
from engine.backend.adapters.implementations.excel_adapter import ExcelToMarkdownAdapter
from engine.backend.adapters.implementations.pdf_adapter import PdfToImageMarkdownAdapter
from engine.backend.compilers.implementations.docx_compiler import DocxCompilerAdapter
from engine.backend.compilers.implementations.html_compiler import HtmlCompilerAdapter
from engine.backend.compilers.implementations.pdf_compiler import PdfCompilerAdapter
from engine.backend.adapters.implementations.md_adapter import MarkdownAdapter, MermaidMarkdownAdapter

logger = logging.getLogger("doc_engine.cache")

class Engine:
    '''
    Assume que execution plan já está pronto
    Coordena o execução:
    - manter o contexto de execução
    - seleciona o compilador adequado
    - Executa os Steps
    - Armazena os resultados 
    '''
    def __init__(
        self,
        inspection_pipeline: InspectionPipeline,
        plan_context: PlanningContext,
        runtime: RuntimeResolver,
        dependency: DependencyResolver,
        pending: PendingCollector
    ):
        self.inspection_pipeline = inspection_pipeline
        self.plan_context = plan_context
        self.runtime = runtime
        self.dependency = dependency
        self.pending = pending

    def plan(
            self,
            graph: RecipeGraph,
            context: ExecutionContext,
    ) -> bool:
        
        self.inspection_pipeline.inspect_pending_nodes(
            graph,
            self.plan_context
        )
        # changed = True
        # loop_iteractions = 0
        # while changed and (loop_iteractions<25):
        # changed = False
        for _ in range(25):
            for node in graph.nodes.values():
                self.runtime.resolve_node(node, context)

            self.dependency.resolve(
                graph,
                self.plan_context
            )

            self.inspection_pipeline.inspect_pending_nodes(
                graph,
                self.plan_context
            )

            pending = self.pending.collect(graph)
            if pending.resolved:
                return graph
            changed |= pending_result.resolved # node.resolution.changed
            return changed

            # node.resolution.changed = False
            # node.resolution.revision += 1
            # loop_iteractions += 1

    def execute(
        self,
        plan: ExecutionPlan,
        context: ExecutionContext
    ):
        for step in plan.steps:
            compiler = self.compiler_registry.get_compiler(
                step.node.component.file_format
            )
            compiler.compile(step, context)
            step.node.completed = True

        return context
    




    # def __init__(self,
    #              execution_plan: ExecutionPlan,
    #              adapter_registry: AdapterRegistry | None = None,
    #              compiler_registry: CompilerRegistry | None = None
    #              ):
    #     # Criação do ambiente Jinja2 customizado para suportar os filtros
    #     self.jinja_env = Template("").environment
    #     Sanitizers.register_filters(self.jinja_env)
    #     # Inicializa o cache manager apontando para a pasta output raiz
    #     self.cache = CacheManager(cache_dir="examples/output")        
    #     # 1. Initialize and boots-up the registry Administrator layout
    #     self.registry = adapter_registry or AdapterRegistry()
    #     if adapter_registry is None:
    #         self._bootstrap_adapters()        
    #     # 2. Initialize and boots-up the Output Exporter Registry
    #     self.compiler_registry = compiler_registry or CompilerRegistry()
    #     if compiler_registry is None:
    #         self._bootstrap_compilers()

    def _bootstrap_adapters(self):
        """Initializes default system plugins for file format resolution."""
        self.registry.register_adapter("xlsx", ExcelToMarkdownAdapter())
        self.registry.register_adapter("pdf", PdfToImageMarkdownAdapter())
        self.registry.register_adapter("docx", DocxPostCompileAdapter())
        self.registry.register_adapter("mermaid", MermaidMarkdownAdapter(
            self.cache
        ))
        self.registry.register_adapter("md", MarkdownAdapter(
            jinja_env=self.jinja_env,
            cache_manager=self.cache
        ))

    def _bootstrap_compilers(self):
        """Initializes system plugins for compilation output formats."""
        self.compiler_registry.register_compiler("docx", DocxCompilerAdapter(registry=self.registry))
        self.compiler_registry.register_compiler("pdf", PdfCompilerAdapter(registry=self.registry))
        self.compiler_registry.register_compiler("html", HtmlCompilerAdapter(registry=self.registry))


    #


    def execute(self):
        for step in plan:
            compiler.compile(step)

class DocumentEngine:
    def __init__(self,
                 manifest_path: str,
                 execution_plan: ExecutionPlan,
                 adapter_registry: AdapterRegistry | None = None,
                 compiler_registry: CompilerRegistry | None = None
                 ):
        with open(manifest_path, 'r', encoding='utf-8') as file:
            raw_data = json.load(file)

        self.manifest = RecipeManifest(**raw_data)
        self.parser = MarkdownParser()

        # Criação do ambiente Jinja2 customizado para suportar os filtros
        self.jinja_env = Template("").environment
        Sanitizers.register_filters(self.jinja_env)

        # Inicializa o cache manager apontando para a pasta output raiz
        self.cache = CacheManager(cache_dir="engine/src/doc_engine/output")
        
        # 1. Initialize and boots-up the Registry Administrator layout
        self.registry = adapter_registry or AdapterRegistry()
        if adapter_registry is None:
            self._bootstrap_adapters()
        
        # 2. Initialize and boots-up the Output Exporter Registry
        self.compiler_registry = compiler_registry or CompilerRegistry()
        if compiler_registry is None:
            self._bootstrap_compilers()

    def _bootstrap_adapters(self):
        """Initializes default system plugins for file format resolution."""
        self.registry.register_adapter("xlsx", ExcelToMarkdownAdapter())
        self.registry.register_adapter("pdf", PdfToImageMarkdownAdapter())
        self.registry.register_adapter("docx", DocxPostCompileAdapter())
        self.registry.register_adapter("mermaid", MermaidMarkdownAdapter(
            self.cache
        ))
        self.registry.register_adapter("md", MarkdownAdapter(
            jinja_env=self.jinja_env,
            cache_manager=self.cache
        ))

    def _bootstrap_compilers(self):
        """Initializes system plugins for compilation output formats."""
        self.compiler_registry.register_compiler("docx", DocxCompilerAdapter(registry=self.registry))
        self.compiler_registry.register_compiler("pdf", PdfCompilerAdapter(registry=self.registry))
        self.compiler_registry.register_compiler("html", HtmlCompilerAdapter(registry=self.registry))
        
    def should_render_component(
            self, 
            component: ComponentConfig, 
            user_inputs: Dict[str, Any]
        ) -> bool:
        """Evaluates if a component condition statement resolves to True based on current user answers."""
        if not component.condition:
            return True # Sem condição significa que o bloco sempre entra
        
        try:
            # Cria um contexto limpo avaliando strings de forma segura
            # Exemplo de string: "has_parking == 'Sim'"
            # Passamos as variáveis digitadas pelo usuário como escopo de variáveis locais do eval()
            eval_scope = {k: str(v).strip() for k, v in user_inputs.items()}
            return bool(eval(component.condition, {"__builtins__": None}, eval_scope))
        except Exception as e:
            print(f"[Warning] Failed evaluating condition condition for block '{component.id}': {e}")
            return component.is_required # Fallback para o estado de obrigatoriedade do bloco
        
    def discover_required_fields(self) -> Dict[str, Dict[str, Any]]:
        """
        Scans all template components to build a unified catalog of input parameters.
        Captures fields registered in top of template components and alone variables in body text.
        No caso de variáveis não definidas, assume que ela é do tipo text.
        """
        consolidated_fields = {}
        
        for component in self.manifest.components:
            if component.type == "template":
                if not os.path.exists(component.source):
                    continue
                
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
    
    # def assemble_document(
    #     self,
    #     user_inputs: Dict[str, Any],
    #     output_resource_dir: str
    # ) -> str:

    #     scheduler, final_order = self._build_execution_plan(user_inputs)

    #     self._execute_scheduler(
    #         scheduler=scheduler,
    #         output_resource_dir=output_resource_dir,
    #     )

    #     return self._assemble_output(
    #         scheduler,
    #         final_order,
    #     )

    def assemble_document(
            self,
            user_inputs: Dict[str, Any],
            output_resource_dir: str
            ) -> str:
        """
        Orchestrates the dynamic document construction via an execution task stack.
        (Clean Architecture Entry Point)
        """
        scheduler = TaskScheduler()
        
        # 1. Carrega o manifesto inicial na pilha
        manifest_ordered_ids = self._load_manifest_tasks(scheduler, user_inputs)

        # 2. Consome a pilha até esvaziar (Máquina de Estados)
        while scheduler.has_tasks():
            current_task = scheduler.pop_task()
            if not current_task or current_task.is_completed:
                continue

            # Verifica se está travado por dependências dos filhos
            if self._is_task_blocked(current_task, scheduler):
                scheduler.stack.append(current_task)
                continue

            # Processa o ciclo de vida da tarefa atual
            self._execute_task_lifecycle(current_task, scheduler, output_resource_dir)

        # 3. Remonta as strings de forma linear e ordenada
        return "\n\n".join([scheduler.registry[comp_id].resolved_content for comp_id in manifest_ordered_ids])

    def _load_manifest_tasks(
            self,
            scheduler: TaskScheduler,
            user_inputs: Dict[str, Any]
        ) -> List[str]:
        """Filters the active recipe manifest layout items and prepares the stack matrix."""
        ordered_ids = []
        for component in self.manifest.components:
            if self.should_render_component(component, user_inputs):
                ordered_ids.append(component.id)
                task = ExecutionTask(
                    id=component.id,
                    source_path=component.source,
                    file_format=component.file_format if component.type == "external" else "md",
                    context_data=user_inputs
                )
                scheduler.push_task(task)
        return ordered_ids

    def _is_task_blocked(self, task: ExecutionTask, scheduler: TaskScheduler) -> bool:
        """Evaluates if the task has children that must finish compilation beforehand."""
        return any(not scheduler.registry[d].is_completed for d in task.depends_on)

    def _execute_task_lifecycle(self, task: ExecutionTask, scheduler: TaskScheduler, output_dir: str):
        """Dispatches polymorphic conversions based on layout design constraints."""
        if task.file_format == "md":
            self._process_markdown_task(task, scheduler, output_dir)
        else:
            # Arquivos puros (Excel, PDF, Imagens) rodam direto
            adapter = self.registry.get_adapter(task.file_format)
            task.resolved_content = adapter.convert(task.source_path, output_dir)
            task.is_completed = True

    def _process_markdown_task(
            self,
            task: ExecutionTask,
            scheduler: TaskScheduler,
            output_dir: str
        ):
        """Handles deep multi-pass rendering injections for Markdown templates."""
        
        def inline_stack_resolver(file_path: str, format_type: str) -> str:
            import hashlib
            sub_task_id = f"sub_{hashlib.md5(file_path.encode()).hexdigest()[:8]}"
            
            if sub_task_id not in scheduler.registry:
                sub_task = ExecutionTask(
                    id=sub_task_id, source_path=file_path, file_format=format_type, context_data=task.context_data
                )
                scheduler.push_task(sub_task)
                task.depends_on.append(sub_task_id)
                return f"<!-- WAIT_FOR:{sub_task_id} -->"
            
            if scheduler.registry[sub_task_id].is_completed:
                return scheduler.get_resolved_value(sub_task_id)
            
            return f"<!-- WAIT_FOR:{sub_task_id} -->"

        md_adapter = MarkdownAdapter(self.jinja_env, self.cache)
        
        content = md_adapter.render_and_compile(
            source_path=task.source_path, user_inputs=task.context_data,
            output_resource_dir=output_dir, external_resolver=inline_stack_resolver
        )
        
        # Se gerou novas dependências inline, joga de volta para esperar o próximo ciclo
        if any(f"<!-- WAIT_FOR:" in content for d in task.depends_on):
            scheduler.stack.append(task)
            return

        # Substituição final dos valores processados
        for dep_id in task.depends_on:
            content = content.replace(f"<!-- WAIT_FOR:{dep_id} -->", scheduler.get_resolved_value(dep_id))

        task.resolved_content = content
        task.is_completed = True

    #LIFO (Last in, First out)
    def assemble_document(self, user_inputs: Dict[str, Any], output_resource_dir: str) -> str:
        scheduler = TaskScheduler()
        final_ordered_component_ids = []

        # Step 1: Empilhamento Inicial (Carga do Manifesto)
        for component in self.manifest.components:
            if not self.should_render_component(component, user_inputs):
                continue
            
            final_ordered_component_ids.append(component.id)
            
            # Criamos a tarefa inicial para cada componente do manifesto
            task = ExecutionTask(
                id=component.id,
                source_path=component.source,
                file_format=component.file_format if component.type == "external" else "md",
                context_data=user_inputs
            )
            scheduler.push_task(task)

        # Step 2: Loop de Execução da Pilha (A Máquina de Estado)
        # O loop consome a pilha. Se uma tarefa gerar sub-tarefas, elas entram no topo e são resolvidas antes.
        while scheduler.has_tasks():
            current_task = scheduler.pop_task()
            if not current_task or current_task.is_completed:
                continue

            # Se a tarefa depende de outras que ainda não foram completadas, ela volta para a pilha
            unresolved_dependencies = [d for d in current_task.depends_on if not scheduler.registry[d].is_completed]
            if unresolved_dependencies:
                # Devolve para a pilha para esperar as sub-tarefas terminarem
                scheduler.stack.append(current_task)
                continue

            # Execução Polimórfica baseada no formato da Tarefa
            if current_task.file_format == "md":
                # Se for template Markdown, criamos a função de interceptação (resolver) que empilha dinamicamente!
                def inline_stack_resolver(file_path: str, format_type: str) -> str:
                    import hashlib
                    # Gera um ID único para a sub-tarefa baseada no path
                    sub_task_id = f"sub_{hashlib.md5(file_path.encode()).hexdigest()[:8]}"
                    
                    if sub_task_id not in scheduler.registry:
                        sub_task = ExecutionTask(
                            id=sub_task_id,
                            source_path=file_path,
                            file_format=format_type,
                            context_data=current_task.context_data
                        )
                        # EMPILHA A SUB-TAREFA NO TOPO. Ela vai travar a execução do MD atual.
                        scheduler.push_task(sub_task)
                        current_task.depends_on.append(sub_task_id)
                        return f"<!-- WAIT_FOR:{sub_task_id} -->" # Placeholder temporário
                    
                    # Se ela já passou pelo ciclo e está pronta, o Markdown captura o valor resolvido
                    if scheduler.registry[sub_task_id].is_completed:
                        return scheduler.get_resolved_value(sub_task_id)
                    
                    return f"<!-- WAIT_FOR:{sub_task_id} -->"

                md_adapter = MarkdownAdapter(self.jinja_env, self.cache)
                
                # Primeira passada do Markdown (Descobrindo shortcodes)
                content = md_adapter.render_and_compile(
                    source_path=current_task.source_path,
                    user_inputs=current_task.context_data,
                    output_resource_dir=output_resource_dir,
                    external_resolver=inline_stack_resolver
                )
                
                # Se após rodar o Jinja, o Markdown percebeu que gerou dependências (tags WAIT_FOR),
                # nós NÃO damos ela como completada. Devolvemos ela para a pilha e reexecutamos o loop.
                if any(f"<!-- WAIT_FOR:" in content for d in current_task.depends_on):
                    scheduler.stack.append(current_task) # Joga de volta para esperar as crianças
                    continue
                
                # Segunda passada: Substitui os placeholders pelos conteúdos reais que já foram computados
                for dep_id in current_task.depends_on:
                    placeholder = f"<!-- WAIT_FOR:{dep_id} -->"
                    resolved_str = scheduler.get_resolved_value(dep_id)
                    content = content.replace(placeholder, resolved_str)

                current_task.resolved_content = content
                current_task.is_completed = True

            else:
                # Tarefas normais (Excel, PDF, Imagem, Mermaid isolado) rodam direto e completam
                adapter = self.registry.get_adapter(current_task.file_format)
                current_task.resolved_content = adapter.convert(current_task.source_path, output_resource_dir)
                current_task.is_completed = True

        # Step 3: Remontagem estrutural na ordem original do Manifesto
        # Como a pilha inverte a ordem ao consumir, nós usamos o mapa final_ordered_component_ids para garantir o layout correto
        assembled_segments = []
        for comp_id in final_ordered_component_ids:
            assembled_segments.append(scheduler.registry[comp_id].resolved_content)

        return "\n\n".join(assembled_segments)

    # Adicione este método dentro da classe DocumentEngine:
    # def pre_process_markdown_diagrams(self, raw_markdown: str, output_resource_dir: str) -> str:
    #     """
    #     Scans the consolidated markdown string, extracts every ```mermaid block,
    #     converts it to a local PNG using the Mermaid adapter, and rewrites the content.
    #     """
    #     # Regex to capture content inside ```mermaid <content> ```
    #     mermaid_pattern = r'```mermaid\s*\n(.*?)\n```'
        
    #     matches = re.findall(mermaid_pattern, raw_markdown, re.DOTALL)
    #     if not matches:
    #         return raw_markdown

    #     processed_markdown = raw_markdown
    #     for index, diagram_code in enumerate(matches):
    #         diagram_id = f"mermaid_diagram_{index + 1}"
    #         # Define a unique name and path for each diagram image asset
    #         image_filename = f"rendered_diagram_{index + 1}.png"
    #         output_image_path = os.path.join(output_resource_dir, image_filename)
            
    #         # Process diagram text into image link using our adapter logic
    #         # image_markdown_tag = MermaidMarkdownAdapter.process_inline_diagram(
    #         #     diagram_code, output_image_path
    #         # )
    #         # 1. Calcula hash do texto do diagrama
    #         diagram_hash = self.cache.calculate_text_hash(diagram_code)
            
    #         # 2. Se o diagrama for idêntico e o PNG existir, pula a chamada da API
    #         if self.cache.is_cached(diagram_id, diagram_hash, [output_image_path]):
    #             logger.info(f"Cache hit for layout {diagram_id}. Reusing local PNG graphic structure.")
    #             image_markdown_tag = f"\n\n![System Diagram]({output_image_path})\n\n"
    #         else:
    #             # Cache miss: aciona a API externa via adaptador
    #             from engine.src.doc_engine.core.adapters import MermaidMarkdownAdapter
    #             image_markdown_tag = MermaidMarkdownAdapter.process_inline_diagram(
    #                 diagram_code, output_image_path
    #             )
    #             # Salva o novo estado no cache
    #             self.cache.update_cache(diagram_id, diagram_hash, [output_image_path])
            
    #         # Replace the code block with the new image tag in the final document text
    #         # We target the specific block to avoid accidental double replacements
    #         full_block_to_replace = f"```mermaid\n{diagram_code}\n```"
    #         processed_markdown = processed_markdown.replace(full_block_to_replace, image_markdown_tag)
            
    #     return processed_markdown

    def assemble_document(self, user_inputs: Dict[str, Any], output_resource_dir: str) -> str:
        """Processes dynamic blocks, handles placeholder values, and bundles text segments."""
        assembled_segments = []
        md_adapter = self.registry.get_adapter('md')

        for component in self.manifest.components:
            # AVALIAÇÃO CONDICIONAL: Se a regra falhar, o bloco é completamente ignorado
            if not self.should_render_component(component, user_inputs):
                print(f"[Engine] Skipping conditional block: '{component.id}' (Condition check failed)")
                continue

            if component.type == "template":
                if not os.path.exists(component.source):
                    raise FileNotFoundError(f"Component file missing: {component.source}")
                
                # O adaptador devolve o texto pronto: Variáveis injetadas E diagramas convertidos!
                compiled_content = md_adapter.convert(
                    source_path=component.source,
                    output_dir=output_resource_dir,
                    user_inputs=user_inputs
                )
                
                # assembled_segments.append(compiled_content)

                # _, body = self.parser.parse_front_matter(component.source)
                # # Usamos o ambiente Jinja que possui nossos filtros registrados
                # jinja_template = self.jinja_env.from_string(body)
                # assembled_segments.append(jinja_template.render(user_inputs))
                # jinja_template = Template(body)
                # rendered_text = jinja_template.render(user_inputs)
                # assembled_segments.append(rendered_text)
                
            elif component.type == "external":
                if not os.path.exists(component.source):
                    print(f"[Warning] File asset path unavailable: {component.source}")
                    continue
                # 1. Calcula o fingerprint do arquivo externo antes de processá-lo
                file_hash = self.cache.calculate_file_hash(component.source)
                
                # Para arquivos como PDF, prevemos que a página 1 em PNG existirá se estiver cacheado
                base_name = os.path.splitext(os.path.basename(component.source))[0]
                # sample_output = os.path.join(output_resource_dir, f"{base_name}_page_1.png")
                # expected_files = [sample_output] if component.file_format == "pdf" else []
                if component.file_format == "pdf":
                    sample_output = os.path.join(output_resource_dir, f"{base_name}_page_1.png")
                elif component.file_format == "mermaid":
                    sample_output = os.path.join(output_resource_dir, f"rendered_{base_name}.png")
                else:
                    sample_output = ""

                expected_files = [sample_output] if sample_output else []
                # 2. Avalia hit do cache
                if self.cache.is_cached(component.id, file_hash, expected_files):
                    logger.info(f"Cache hit for external component '{component.id}'. Skipping adapter rendering step.")
                    # Arquivos markdown ou excel precisam ler os arquivos ou gerar strings de texto, 
                    # mas para fins do MVP focaremos o cache nos gargalos pesados: PDF e Imagens.
                    if component.file_format not in ["pdf", "image"]:
                        adapter = self.registry.get_adapter(component.file_format)
                        converted_content = adapter.convert(component.source, output_resource_dir)
                        assembled_segments.append(converted_content)
                        continue

                # Dynamic strategy execution - pure polymorphic call
                # Engine doesn't know HOW it translates, it just triggers the Port contract
                adapter = self.registry.get_adapter(component.file_format)
                converted_content = adapter.convert(component.source, output_resource_dir)
                assembled_segments.append(converted_content)

                # Static entry marker placeholder for downstream native compiler binding
                # assembled_segments.append(f"\n\n<!-- ATTACH EXTERNAL FILE: {component.source} -->\n\n")
                
                # 3. Registra ou atualiza o cache pós execução de sucesso
                self.cache.update_cache(component.id, file_hash, expected_files)

        return "\n\n".join(assembled_segments)