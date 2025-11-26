"""
IR - Código Intermediário
Three-Address Code (TAC) e Quádruplas
"""

from .ir import TAC, IRProgram
from .ir_generator import IRGenerator

__all__ = ['TAC', 'IRProgram', 'IRGenerator']
