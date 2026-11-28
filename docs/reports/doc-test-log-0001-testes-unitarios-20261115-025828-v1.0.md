---
id: "doc-test-log-0001-testes-unitarios-20261115-025828-v1.0"
type: "doc-test-log"
title: "Relatório Testes Unitários"
version: "1.0"
status: "rascunho"
canonical: false
canonical_slug: "testes-unitarios-20261115-025828"
created: "2026-11-15"
updated: "2026-11-15"
author: "COBECO Hook (script-hooks-0002)"
owner: "CCB"
ratified_by: null
ratified_at: null
supersedes: null
superseded_by: null
trace:
  constitution: ["constitution-0001-constitution-canon.md"]
  req_func: []
  req_nfunc: []
  use_cases: []
  specs: []
  handoffs: []
  adrs: []
  code: ["scripts/script-hooks-0002-ciclo-codificacao-deploy-v1.0.py"]
  tests: []
domain: "governance"
layer: "report"
tags: ["relatorio", "hook", "ciclo-codificacao-deploy"]
lgpd_class: "n/a"
workflow:
  stage: "rascunho"
  reviewer: null
  reviewed_at: null
  approval_hash: null
  board_url: null
---
Executado: 2026-11-15T05:58:28.787452Z
Diretório: backend/tests/unit
Resultado: FALHOU

```
============================= test session starts ==============================
platform linux -- Python 3.14.10, pytest-9.2.0, pluggy-1.6.0
benchmark: 5.2.3 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
rootdir: /lab/FATEC/202602/lab_eng_software/COBECO/backend
configfile: pytest.ini
plugins: asyncio-1.5.0, respx-0.23.1, cov-7.1.0, hypothesis-6.152.6, anyio-4.13.0, benchmark-5.2.3, platformdirs-4.14.5
asyncio: mode=Mode.AUTO, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collected 0 items / 9 errors

==================================== ERRORS ====================================
_____________ ERROR collecting tests/unit/domain/test_entities.py ______________
ImportError while importing test module '/lab/FATEC/202602/lab_eng_software/COBECO/backend/tests/unit/domain/test_entities.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/usr/lib/python3.14/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
backend/tests/unit/domain/test_entities.py:7: in <module>
    from src.domain.entities import (
E   ModuleNotFoundError: No module named 'src'
___________ ERROR collecting tests/unit/domain/test_value_objects.py ___________
ImportError while importing test module '/lab/FATEC/202602/lab_eng_software/COBECO/backend/tests/unit/domain/test_value_objects.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/usr/lib/python3.14/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
backend/tests/unit/domain/test_value_objects.py:5: in <module>
    from src.domain.entities import Email, CNPJ, SenhaHash, UnidadeMedida
E   ModuleNotFoundError: No module named 'src'
________________ ERROR collecting tests/unit/test_seed_data.py _________________
ImportError while importing test module '/lab/FATEC/202602/lab_eng_software/COBECO/backend/tests/unit/test_seed_data.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/usr/lib/python3.14/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
backend/tests/unit/test_seed_data.py:17: in <module>
    from script_seed_0001_generate_seed_v1_0 import render_sql
E   ModuleNotFoundError: No module named 'script_seed_0001_generate_seed_v1_0'
________ ERROR collecting tests/unit/usecases/test_cadastrar_usuario.py ________
ImportError while importing test module '/lab/FATEC/202602/lab_eng_software/COBECO/backend/tests/unit/usecases/test_cadastrar_usuario.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/usr/lib/python3.14/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
backend/tests/unit/usecases/test_cadastrar_usuario.py:5: in <module>
    from src.domain.usecases import (
E   ModuleNotFoundError: No module named 'src'
_______ ERROR collecting tests/unit/usecases/test_calcular_orcamento.py ________
ImportError while importing test module '/lab/FATEC/202602/lab_eng_software/COBECO/backend/tests/unit/usecases/test_calcular_orcamento.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/usr/lib/python3.14/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
backend/tests/unit/usecases/test_calcular_orcamento.py:7: in <module>
    from src.domain.usecases import (
E   ModuleNotFoundError: No module named 'src'
___________ ERROR collecting tests/unit/usecases/test_criar_lista.py ___________
ImportError while importing test module '/lab/FATEC/202602/lab_eng_software/COBECO/backend/tests/unit/usecases/test_criar_lista.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/usr/lib/python3.14/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
backend/tests/unit/usecases/test_criar_lista.py:6: in <module>
    from src.domain.usecases import (
E   ModuleNotFoundError: No module named 'src'
______________ ERROR collecting tests/unit/usecases/test_login.py ______________
ImportError while importing test module '/lab/FATEC/202602/lab_eng_software/COBECO/backend/tests/unit/usecases/test_login.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/usr/lib/python3.14/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
backend/tests/unit/usecases/test_login.py:6: in <module>
    from src.domain.usecases import (
E   ModuleNotFoundError: No module named 'src'
_____________ ERROR collecting tests/unit/usecases/test_logout.py ______________
ImportError while importing test module '/lab/FATEC/202602/lab_eng_software/COBECO/backend/tests/unit/usecases/test_logout.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/usr/lib/python3.14/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
backend/tests/unit/usecases/test_logout.py:5: in <module>
    from src.domain.usecases import LogoutUseCase
E   ModuleNotFoundError: No module named 'src'
_________ ERROR collecting tests/unit/usecases/test_recuperar_senha.py _________
ImportError while importing test module '/lab/FATEC/202602/lab_eng_software/COBECO/backend/tests/unit/usecases/test_recuperar_senha.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/usr/lib/python3.14/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
backend/tests/unit/usecases/test_recuperar_senha.py:5: in <module>
    from src.domain.usecases import (
E   ModuleNotFoundError: No module named 'src'
=============================== warnings summary ===============================
../../../../../home/leonardo/.local/lib/python3.14/site-packages/anyio/pytest_plugin.py:14
  /home/leonardo/.local/lib/python3.14/site-packages/anyio/pytest_plugin.py:14: PytestRemovedIn10Warning: _pytest.python.CallSpec2 has been renamed to CallSpec.
  The CallSpec2 alias will be removed in pytest 10.
  Update imports to use CallSpec instead.
  See https://docs.pytest.org/en/stable/deprecations.html#callspec2-renamed
    from _pytest.python import CallSpec2

../../../../../home/leonardo/.local/lib/python3.14/site-packages/pytest_benchmark/plugin.py:260
  /home/leonardo/.local/lib/python3.14/site-packages/pytest_benchmark/plugin.py:260: PendingDeprecationWarning: FileType is deprecated. Simply open files after parsing arguments.
    type=argparse.FileType('wb'),

../../../../../home/leonardo/.local/lib/python3.14/site-packages/_pytest/cacheprovider.py:487
  /home/leonardo/.local/lib/python3.14/site-packages/_pytest/cacheprovider.py:487: PytestCacheWarning: could not create cache path /lab/FATEC/202602/lab_eng_software/COBECO/backend/.pytest_cache/v/cache/nodeids: [Errno 13] Permission denied: '/lab/FATEC/202602/lab_eng_software/COBECO/backend/.pytest_cache/v'
    config.cache.set("cache/nodeids", sorted(str(n) for n in self.cached_nodeids))

../../../../../home/leonardo/.local/lib/python3.14/site-packages/_pytest/cacheprovider.py:439
  /home/leonardo/.local/lib/python3.14/site-packages/_pytest/cacheprovider.py:439: PytestCacheWarning: could not create cache path /lab/FATEC/202602/lab_eng_software/COBECO/backend/.pytest_cache/v/cache/lastfailed: [Errno 13] Permission denied: '/lab/FATEC/202602/lab_eng_software/COBECO/backend/.pytest_cache/v'
    config.cache.set("cache/lastfailed", current_lastfailed)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=========================== short test summary info ============================
ERROR backend/tests/unit/domain/test_entities.py
ERROR backend/tests/unit/domain/test_value_objects.py
ERROR backend/tests/unit/test_seed_data.py
ERROR backend/tests/unit/usecases/test_cadastrar_usuario.py
ERROR backend/tests/unit/usecases/test_calcular_orcamento.py
ERROR backend/tests/unit/usecases/test_criar_lista.py
ERROR backend/tests/unit/usecases/test_login.py
ERROR backend/tests/unit/usecases/test_logout.py
ERROR backend/tests/unit/usecases/test_recuperar_senha.py
!!!!!!!!!!!!!!!!!!! Interrupted: 9 errors during collection !!!!!!!!!!!!!!!!!!!!
======================== 4 warnings, 9 errors in 0.17s =========================
/home/leonardo/.local/lib/python3.14/site-packages/pytest_asyncio/plugin.py:306: PytestDeprecationWarning: The configuration option "asyncio_default_fixture_loop_scope" is unset.
The event loop scope for asynchronous fixtures will default to the fixture scope. Future versions of pytest-asyncio will default the loop scope for asynchronous fixtures to "function" scope. Set the default fixture loop scope explicitly in order to avoid unexpected behavior in the future. Valid fixture loop scopes are: "function", "class", "module", "package", "session". Set it to "fixture-scope" to keep the current behavior.

  warnings.warn(PytestDeprecationWarning(_DEFAULT_FIXTURE_LOOP_SCOPE_UNSET))

```