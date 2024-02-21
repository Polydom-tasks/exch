"""Module containing symbols validator."""

from dataclasses import dataclass

ALLOWED_SYMBOL_LENGTH = 3


@dataclass
class SymbolsValidator:
    """Validate symbols."""

    symbols: str

    async def is_valid(self) -> bool:
        """Validate symbols length."""
        return all([len(symbol) == ALLOWED_SYMBOL_LENGTH for symbol in self.symbols.split(",")])
