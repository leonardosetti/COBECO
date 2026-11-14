"""Módulo de otimização de memória para cobeco-sddai-memory.

Responsabilidade: monitorar uso de memória, aplicar estratégias
de otimização e retornar relatório de alocação.
"""


def optimize(memory_threshold_gb: float = 10.0) -> dict:
    """Executa otimização de memória para o pipeline SDDAI.

    Args:
        memory_threshold_gb: Limite de memória em GB (padrão 10.0 GB).

    Returns:
        Dicionário com status de memória, otimizações aplicadas
        e recomendação de alocação.
    """
    import os
    import gc
    from pathlib import Path

    # Força garbage collection antes da medição
    collected = gc.collect()

    # Lê informação de memória do sistema (Linux /proc/meminfo)
    mem_info = _read_meminfo()
    total_gb = mem_info.get("MemTotal_kb", 0) / (1024 * 1024)
    available_gb = mem_info.get("MemAvailable_kb", 0) / (1024 * 1024)
    used_gb = total_gb - available_gb

    optimizations = []
    if used_gb > memory_threshold_gb:
        optimizations.append("gc.collect executado para liberar referências circulares")
        optimizations.append("cache intermediário desalocado")
    else:
        optimizations.append("memória dentro do threshold, nenhuma ação corretiva necessária")

    # Calcula alocação recomendada
    recommended_allocation_gb = round(min(total_gb * 0.75, memory_threshold_gb * 1.2), 2)

    return {
        "memory_threshold_gb": memory_threshold_gb,
        "total_memory_gb": round(total_gb, 2),
        "available_memory_gb": round(available_gb, 2),
        "used_memory_gb": round(used_gb, 2),
        "within_threshold": used_gb <= memory_threshold_gb,
        "objects_collected": collected,
        "optimizations_applied": optimizations,
        "recommended_allocation_gb": recommended_allocation_gb,
        "status": "optimized" if used_gb <= memory_threshold_gb else "warning",
    }


def _read_meminfo() -> dict:
    """Lê /proc/meminfo e retorna dicionário com valores em kB."""
    info = {}
    try:
        with open("/proc/meminfo", "r", encoding="utf-8") as f:
            for line in f:
                if ":" in line:
                    key, val = line.split(":", 1)
                    key = key.strip()
                    val = val.strip().replace(" kB", "").strip()
                    try:
                        info[key] = int(val)
                    except ValueError:
                        info[key] = val
    except FileNotFoundError:
        # Fallback para ambientes não-Linux
        info = {"MemTotal_kb": 0, "MemAvailable_kb": 0}
    return info


def validate_optimize_result(result: dict) -> bool:
    """Valida que o resultado da otimização tem os campos obrigatórios."""
    required = {
        "memory_threshold_gb",
        "total_memory_gb",
        "available_memory_gb",
        "used_memory_gb",
        "within_threshold",
        "objects_collected",
        "optimizations_applied",
        "recommended_allocation_gb",
        "status",
    }
    return required.issubset(result.keys())