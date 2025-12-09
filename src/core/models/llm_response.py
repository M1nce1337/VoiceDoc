from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text

from .base import Base


class LLMResponse(Base):
    __tablename__ = "llm_response"

    complaints: Mapped[str] = mapped_column(Text, nullable=False)
    anamnesis: Mapped[str] = mapped_column(Text, nullable=False)
    status_praesens: Mapped[str] = mapped_column(Text, nullable=False)
    recommendations: Mapped[str] = mapped_column(Text, nullable=False)