description = "Adiciona campo payment_method nos pedidos existentes"

async def up(db):
    result = await db.orders.update_many(
        {"payment_method": {"$exists": False}},
        {"$set": {"payment_method": "no_data"}}
    )
    print(f"Atualizados: {result.modified_count} documentos")

async def down(db):
    await db.orders.update_many(
        {},
        {"$unset": {"payment_method": ""}}
    )