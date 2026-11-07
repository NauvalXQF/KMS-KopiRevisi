# KMS Kopi — Knowledge Management System for Coffee-Shop SMEs

A web prototype of a **Knowledge Management System (KMS)** that helps small coffee-shop owners and staff **store, find, share, and reuse operational knowledge** — recipes, SOPs, suppliers, complaints — while tracking stock and sales.

**Live demo:** [https://kms.opankcs.com](https://kms.opankcs.com)

> Academic group project — Information Systems course, Department of Informatics, Diponegoro University (2026).

## Features

**Knowledge**
- Knowledge library by category: recipes & measurements, SOPs, suppliers & ingredients, complaints, sales data
- Keyword search and category filters
- New knowledge entries (title, category, description, photo/video attachment)
- Owner validation flow: pending → approved / revision → published
- Knowledge versioning and status notifications

**Operations**
- Ingredient stock: record in/out movements, low-stock warnings
- Suppliers & ingredients: contact, latest price, rating, storage notes
- Sales per menu item
- Complaint log: type, solution, follow-up

**Dashboard**
- Best-selling menus, peak hours, low stock, pending validations

## Tech stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask, SQLAlchemy |
| Database | MySQL / MariaDB |
| Frontend | Jinja templates, server-rendered pages |
| Extras | openpyxl export, python-dotenv config |

## Getting started

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt

# configure database credentials in .env (see .env.example)
python run.py
```

The app runs at `http://localhost:5000` by default.

## Project structure

```
app/            application package (routes, models, templates, static assets)
database/       schema / seed data
requirements.txt
run.py          entry point
requirements.md requirements traceability (academic deliverable)
changelog.md    change history
```

## Team

Group project for the Information Systems course (2026). Product concept, requirements, and validation flow were developed together with the team; this repository holds the implementation.

## Status

Prototype completed for academic evaluation and deployed for demo purposes.
