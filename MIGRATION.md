# Database Migration Instructions

## If You Get "no such column" Error

This happens when upgrading from Phase 1 to Phase 2 because new database columns were added.

### Solution: Run the Migration Script

```bash
python migrate_db.py
```

This will:
- Add new columns to existing tables
- Create new tables (expenses, saved_destinations)
- Preserve all your existing data

### Alternative: Fresh Start

If you want to start fresh (loses all data):

1. Delete the database:
```bash
# Windows
del database\traveloop.db

# Mac/Linux
rm database/traveloop.db
```

2. Run the app (it will create a new database):
```bash
python app.py
```

### What the Migration Adds

**Users table:**
- profile_picture
- language
- dark_mode

**Trips table:**
- destination_country
- status
- is_archived

**Activities table:**
- category
- duration

**New tables:**
- expenses
- saved_destinations

---

After migration, your app will work with all Phase 2 features!
