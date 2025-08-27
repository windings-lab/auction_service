import asyncio

async def upgrade(revision="head"):
    from alembic import command
    from alembic.config import Config

    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, revision)

asyncio.run(upgrade("head"))

if __name__ == "__main__":
    asyncio.run(upgrade())