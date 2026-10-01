"""Embute docz_core e docz_application dentro do wheel de docz-cli."""
from pathlib import Path

from hatchling.builders.hooks.plugin.interface import BuildHookInterface

# pacote importável -> pasta do membro dentro de packages/
BUNDLED = {
    "dcp_engine": "dcp-engine",
    "dcp_application": "dcp-application",
}


class CustomBuildHook(BuildHookInterface):
    def initialize(self, version, build_data):
        # Em instalações editáveis (uv sync), core e application já são
        # membros editáveis do workspace. Por precaução, não copiamos nada
        # para não criar cópias estáticas que escondam o código-fonte real.
        if version != "standard":
            return

        packages_dir = Path(self.root).resolve().parent
        for import_name, folder in BUNDLED.items():
            source = packages_dir / folder / "src" / import_name
            if not source.is_dir():
                raise RuntimeError(
                    f"Não encontrei {source}. Construa o wheel direto do monorepo: "
                    "uv build --package dcp-cli --wheel"
                )
            # origem (caminho absoluto) -> destino dentro do wheel
            build_data["force_include"][str(source)] = import_name