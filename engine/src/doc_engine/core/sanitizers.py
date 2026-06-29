import datetime
import logging
from typing import Any

logger = logging.getLogger("doc_engine.sanitizers")

class DocumentSanitizers:
    """Collection of data formatting filters for professional document outputs."""

    @staticmethod
    def to_currency(value: Any) -> str:
        """Formats a raw number into Brazilian Currency (R$). E.g., 1500.5 -> R$ 1.500,50"""
        try:
            if value is None or value == "":
                return ""
            num = float(str(value).replace(",", ".").strip())
            return f"R$ {num:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        except Exception as e:
            logger.warning(f"Failed to apply currency filter to '{value}': {e}")
            return str(value)

    @staticmethod
    def to_decimal(value: Any) -> str:
        """Formats a number with standard thousands separators and two decimals. E.g., 12500 -> 12.500,00"""
        try:
            if value is None or value == "":
                return ""
            num = float(str(value).replace(",", ".").strip())
            return f"{num:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        except Exception as e:
            return str(value)

    @staticmethod
    def to_long_date(value: Any) -> str:
        """Transforms YYYY-MM-DD string into a standard long text Portuguese date."""
        try:
            if not value:
                return ""
            date_obj = datetime.datetime.strptime(str(value).strip(), "%Y-%m-%d")
            months = [
                "janeiro", "fevereiro", "março", "abril", "maio", "junho",
                "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"
            ]
            return f"{date_obj.day} de {months[date_obj.month - 1]} de {date_obj.year}"
        except Exception as e:
            logger.warning(f"Failed to parse date filter for '{value}': {e}")
            return str(value)

    @classmethod
    def register_filters(cls, jinja_env: Any):
        """Binds all methods within this class as active filters inside the Jinja Environment."""
        jinja_env.filters["currency"] = cls.to_currency
        jinja_env.filters["decimal"] = cls.to_decimal
        jinja_env.filters["long_date"] = cls.to_long_date