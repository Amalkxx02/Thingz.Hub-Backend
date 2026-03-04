from sqlalchemy.ext.asyncio import AsyncSession

async def db_execution(db: AsyncSession, stmt):
    try:
        await db.execute(stmt)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise e