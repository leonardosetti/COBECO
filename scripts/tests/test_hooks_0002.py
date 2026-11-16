#!/usr/bin/env python3
"""Self-check do hook 0002 (rodar: python3 scripts/tests/test_hooks_0002.py)."""

import importlib.util
import sys
import tempfile
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPTS = ROOT / "scripts"


def carregar(nome: str, caminho: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(nome, caminho)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


hook = carregar(
    "hook_0002", SCRIPTS / "script-hooks-0002-ciclo-codificacao-deploy-v1.0.py"
)


def test_plano_ondas_sem_ciclo() -> None:
    deps = {"a": [], "b": ["a"], "c": ["a"]}
    ordem, ciclo = hook.plano_ondas(deps)
    assert ciclo == set()
    assert ordem[0] == "a"
    assert set(ordem) == {"a", "b", "c"}
    assert ordem.index("a") < ordem.index("b")
    assert ordem.index("a") < ordem.index("c")


def test_plano_ondas_com_ciclo() -> None:
    ordem, ciclo = hook.plano_ondas({"a": ["b"], "b": ["a"], "c": []})
    assert set(ciclo) == {"a", "b"}
    assert ordem == ["c"]


def test_relatorio_p1_p2_valido() -> None:
    val = carregar("artifact_validate", SCRIPTS / "artifact_validate.py")
    with tempfile.TemporaryDirectory() as tmp:
        setattr(hook, "REPORTS_DIR", Path(tmp))
        md, js = hook.emitir_relatorio(
            "doc-test-log",
            "testes-unitarios-20260101-000000",
            "Relatório Testes Unitários",
            "# corpo\n",
            {"resultado": "passou"},
        )
        assert js.exists()
        r = val.validate_file(md)
        assert r.valid, f"relatório viola P1/P2: {r.errors}"
        assert not r.errors


def main() -> int:
    testes = [
        (n, f)
        for n, f in sorted(globals().items())
        if n.startswith("test_") and callable(f)
    ]
    falhas = 0
    for nome, fn in testes:
        try:
            fn()
            print(f"✅ {nome}")
        except AssertionError as e:
            print(f"❌ {nome}: {e}")
            falhas += 1
    print(f"\n{len(testes) - falhas}/{len(testes)} testes OK")
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
