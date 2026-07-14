from contextlib import contextmanager
from typing import ClassVar, Iterator

from pydantic import BaseModel, PrivateAttr

from engine.backend.ir.block import ComponentIRBlock, IRBlock
from engine.frontend.syntax.parsed_markdown import ParsedMarkdown
from engine.runtime.markdown_assembler import MarkdownAssembler


class DocumentIR(BaseModel):
    ROOT_ID: ClassVar[str] = "__document_root__"
    
    version: str = "1.0"
    root: IRBlock

    _blocks: dict[str, IRBlock] = PrivateAttr(default_factory=dict)
    _nodes: dict[str, IRBlock] = PrivateAttr(default_factory=dict)
    _transaction_depth: int = PrivateAttr(default=0)


    @classmethod
    def create(cls) -> "DocumentIR":
        document = cls(
            root=IRBlock()
        )
        document.root._id = cls.ROOT_ID
        document._rebuild_indexes()
        return document
    
    def __setattr__(self, name, value):
        if name == "root" and hasattr(self, "root"):
            raise AttributeError("Document root is immutable.")
        
        super().__setattr__(name, value)
    

    def assemble_document(self) -> ParsedMarkdown:
        assembler = MarkdownAssembler()
        return assembler.assemble(self)
    
    # def model_post_init(self, __context) -> None:
    #     self._rebuild_indexes()

    def _rebuild_indexes(self) -> None:
        self._blocks.clear()
        self._nodes.clear()

        for block in self.root.walk():
            self._blocks[block.id] = block

            if isinstance(block, ComponentIRBlock):
                self._nodes[block.node_id] = block

    @property
    def blocks_ids(self):
        return list(self._blocks.keys())
    
    @property
    def nodes_ids(self):
        return list(self._nodes.keys())
    

    def find(self, block_id: str) -> IRBlock | None:
        block = self._blocks.get(block_id, None)
        return block

    def find_by_node(self, node_id: str) -> IRBlock | None:
        block = self._nodes.get(node_id, None)
        return block
    
    def walk(self) -> Iterator[IRBlock]:
        # yield self
        yield from self.root.walk()
        
    def descendants(self, block: IRBlock) -> list[IRBlock]:
        descendants: list[IRBlock] = []

        def visit(node: IRBlock):
            for child in node.children:
                descendants.append(child)
                visit(child)

        visit(block)

        return descendants
    
    def descendants_by_id(
        self,
        block_id: str
    ) -> list[IRBlock]:

        block = self.find(block_id)

        if block is None or block is not self.root:
            raise ValueError(f"Block '{block_id}' not found.")

        return self.descendants(block)
    
    def append(
        self,
        parent_id: str,
        block: IRBlock
    ) -> None:
        parent = self.find(parent_id)
        if parent is None:
            raise ValueError(f"Parent '{parent_id}' not found.")
        
        if block.parent is not None:
            self._detach(block.parent, block)

        self._attach(parent, block)

    def remove(
        self,
        block_id: str
    ) -> IRBlock:
        block = self.find(block_id)

        if block is None:
            raise ValueError(f"Block '{block_id}' not found.")

        if block is self.root:
            raise ValueError("Cannot remove root block.")

        parent = block._parent

        if parent is not None:
            self._detach(parent, block)

        return block


    def move(
        self,
        block_id: str,
        parent_id: str,
        index: int | None = None
    ) -> None:
        block = self.find(block_id)
        parent = self.find(parent_id)

        if block is None:
            raise ValueError(f"Block '{block_id}' not found.")

        if parent is None:
            raise ValueError(f"Parent '{parent_id}' not found.")

        if block is self.root:
            raise ValueError("Cannot move root block.")

        #
        # Evita ciclos
        #
        ancestor = parent
        while ancestor is not None:
            if ancestor is block:
                raise ValueError(
                    "Cannot move a block into one of its descendants."
                )
            ancestor = ancestor._parent

        if block._parent is not None:
            self._detach(block._parent, block)

        if index is None or index >= len(parent._children):
            self._attach(parent, block)
            return
        
        self._attach_at(parent, block, index)

        # block._parent = parent
        # parent._children.insert(index, block)


    def replace(
        self,
        block_id: str,
        new_block: IRBlock
    ) -> None:
        block = self.find(block_id)

        if block is None:
            raise ValueError(f"Block '{block_id}' not found.")

        if block is self.root:
            raise ValueError("Cannot replace root block.")

        parent = block.parent
        index = parent.children.index(block)

        self._detach(parent, block)

        self._attach_at(parent, new_block, index)
        # new_block._parent = parent
        # parent._children.insert(index, new_block)


    def insert_before(
        self,
        target_id: str,
        block: IRBlock
    ):
        target = self.find(target_id)

        if target is None:
            raise ValueError(f"Block '{target_id}' not found.")

        if target is self.root:
            raise ValueError("Cannot insert before root block.")

        parent = target._parent
        index = parent._children.index(target)

        if block.parent is not None:
            self._detach(block._parent, block)

        self._attach_at(parent, block, index)
        # block._parent = parent
        # parent._children.insert(index, block)

    def insert_after(
        self,
        target_id: str,
        block: IRBlock
    ):
        target = self.find(target_id)

        if target is None:
            raise ValueError(f"Block '{target_id}' not found.")

        if target is self.root:
            raise ValueError("Cannot insert after root block.")

        parent = target.parent
        index = parent.children.index(target) + 1

        if block.parent is not None:
            self._detach(block.parent, block)

        block._parent = parent
        parent._children.insert(index, block)
    
    def _attach(self, parent, child):
        child._parent = parent
        parent._children.append(child)
        self._blocks[child.id] = child
    
        if hasattr(child, "node_id"):
            self._nodes[child.node_id] = child

    def _attach_at(
        self,
        parent: IRBlock,
        child: IRBlock,
        index: int
    ):
        child._parent = parent
        parent._children.insert(index, child)
        self._blocks[child.id] = child

        if hasattr(child, "node_id"):
            self._nodes[child.node_id] = child
        
    def _detach(self, parent, child):
        parent._children.remove(child)
        child._parent = None
        self._blocks.pop(child.id)

        if hasattr(child, "node_id"):
            self._nodes.pop(child.node_id)
    
    def _validate(self) -> None:
        visited: set[str] = set()

        def visit(
            node: IRBlock,
            parent: IRBlock | None
        ) -> None:
            # ids duplicados
            if node.id in visited:
                raise ValueError(
                    f"Duplicated block id '{node.id}'."
                )

            visited.add(node.id)
            # parent consistente
            if node.parent is not parent:
                raise ValueError(f"Invalid parent for block '{node.id}'.")
            
            children_ids: set[str] = set()
            # filhos consistentes
            for child in node.children:
                if child is node:
                    raise ValueError(f"Block '{node.id}' cannot be its own child.")
                
                if child.id in children_ids:
                    raise ValueError(f"Duplicated child '{child.id}' in '{node.id}'.")
                
                children_ids.add(child.id)

                visit(child, node)

        if self.root.parent is not None:
            raise ValueError("Root block cannot have a parent.")

        visit(self.root, None)

    def flatten(self) -> list[IRBlock]:
        return list(self.root.walk())
    
    '''
    with ir.transaction():
        ir.move(...)
        ir.remove(...)
        ir.insert(...)
    _validate()
    _rebuild_indexes()
    '''
    
    @contextmanager
    def transaction(self):
        self._transaction_depth += 1
        try:
            yield self

        finally:
            self._transaction_depth -= 1
            if self._transaction_depth == 0:
                self._validate()
        # try:
        #     yield self
        #     self._validate()
        # except Exception:
        #     raise

    def clone(self) -> DocumentIR:
        return self.model_copy(deep=True)