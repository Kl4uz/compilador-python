"""
Optimizer - Otimizações de Código
CSE, Constant Folding, Dead Code Elimination, etc.
"""

from .optimizer import (
    Optimizer,
    OptimizationPass,
    ConstantFolding,
    DeadCodeElimination,
    CopyPropagation,
    CommonSubexpressionElimination
)
from .peephole import PeepholeOptimizer, AlgebraicSimplification

__all__ = [
    'Optimizer',
    'OptimizationPass',
    'ConstantFolding',
    'DeadCodeElimination',
    'CopyPropagation',
    'CommonSubexpressionElimination',
    'PeepholeOptimizer',
    'AlgebraicSimplification'
]
