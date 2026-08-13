# Personal Finance Dashboard

A full-stack personal finance tracker built with Django and MySQL. Tracks multiple accounts, categorized income/expense transactions, budgets, savings goals, and recurring bills, with a live dashboard and CSV import/export.

## Features

- Multi-account tracking (Bank, Cash, Credit Card, Wallet, Investment) with currency-aware balances
- Income/expense/transfer transactions with atomic, race-condition-safe balance updates
- Categories and subcategories with rule-based auto-categorization
- Budgets with live progress tracking and overspend alerts
- Savings goals with account-linked contributions
- CSV import/export with all-or-nothing atomic imports
- Dashboard with net worth, monthly income/expense trends, and category breakdown charts
- Recurring transactions with automatic generation and email bill reminders
- Soft deletes with an audit trail on all financial records, and an admin restore workflow
- Dark/light mode

## Tech Stack

- **Backend:** Django 5.2 (LTS)
- **Database:** MySQL 8.0
- **Frontend:** Django templates, Tailwind CSS (CDN), Chart.js
- **Scheduling:** Django management command + OS-level task scheduler (no external broker required)

## Setup

1. Clone the repository and create a virtual environment:

   ```bash
   python -m venv venv
   venv\Scripts\activate   # Windows
   pip install -r requirements.txt
   ```

2. Create a MySQL database and user, then create a `.env` file in the project root:

   ```
   DB_NAME=finance_dashboard
   DB_USER=finance_user
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=3306
   SECRET_KEY=your_secret_key
   DEBUG=True
   ```

3. Run migrations and create a superuser:

   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

4. Start the development server:

   ```bash
   python manage.py runserver
   ```

## Running Tests

```bash
python manage.py test
```

## Recurring Transactions

The `process_recurring` management command generates due recurring transactions and sends email reminders for bills due within 3 days:

```bash
python manage.py process_recurring
```

Schedule this to run daily via Windows Task Scheduler (or cron on Linux/macOS) for automatic processing.

## Project Structure

- `core/` — shared base models (soft delete, audit trail), dashboard view, middleware
- `accounts/` — bank/cash/credit accounts and currencies
- `transactions/` — transactions, categories, auto-categorization rules, recurring transactions, CSV import/export
- `budgets/` — budget tracking and overspend calculation
- `goals/` — savings goals
- `users/` — authentication (signup/login/logout)

## License

This project is for personal/educational use.