from db import get_db

def save_history(
    user_id,
    source,
    asset,
    asset_type,
    signal,
    confidence,
    result
):
    db = get_db()
    db.execute("""
        INSERT INTO history
        (user_id, source, asset, asset_type, signal, confidence, result)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        source,
        asset,
        asset_type,
        signal,
        confidence,
        result
    ))
    db.commit()
