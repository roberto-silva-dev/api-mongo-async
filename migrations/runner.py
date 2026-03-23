import asyncio
import importlib
import os
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorClient
import sys
from app.config import settings


async def run_migrations(rollback=False):
    client = AsyncIOMotorClient(settings.mongo_url)
    db = client[settings.mongo_db]

    if rollback:
        last = await db.migrations.find_one(
            sort=[("executed_at", -1)]
        )

        if not last:
            print("Nenhuma migration para reverter")
            return

        print(f"Revertendo {last['name']}...")
        module = importlib.import_module(f"migrations.{last['name']}")
        await module.down(db)

        await db.migrations.delete_one({"name": last["name"]})
        print(f"{last['name']} revertida")

    else:
        executed = await db.migrations.distinct("name")

        files = sorted([
            f[:-3] for f in os.listdir(os.path.dirname(__file__))
            if f.endswith(".py") and f != "runner.py"
        ])

        for filename in files:
            if filename in executed:
                print(f"Skipping {filename} — já executada")
                continue

            print(f"Rodando {filename}...")
            module = importlib.import_module(f"migrations.{filename}")
            await module.up(db)

            await db.migrations.insert_one({
                "name": filename,
                "executed_at": datetime.now(timezone.utc),
                "description": getattr(module, "description", "")
            })
            print(f"{filename} concluída")

    client.close()

# python -m migrations.runner         → roda pendentes
# python -m migrations.runner rollback → reverte última
rollback = len(sys.argv) > 1 and sys.argv[1] == "rollback"
asyncio.run(run_migrations(rollback))