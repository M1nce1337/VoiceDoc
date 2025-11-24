from sqlalchemy.ext.asyncio import AsyncSession
from core.models.asr_result import ASRResult

class ASRService:
    @staticmethod
    async def save_record(
        session: AsyncSession,
        raw_text: str,
        final_text: str
    ) -> ASRResult:
        
        record = ASRResult(
            raw_text=raw_text,
            final_text=final_text
        )

        session.add(record)
        await session.commit()
        await session.refresh(record)

        return record