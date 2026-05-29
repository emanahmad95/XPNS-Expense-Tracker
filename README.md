# 💸 XPNS — Expense Tracker

A cinematic, web-based personal expense tracker built with **Python (Flask)** and a dynamic HTML/CSS/JS frontend. XPNS lets you log, categorize, filter, and analyze your spending — all from your browser, with data persisted locally as JSON.

---

## ✨ Features

- **Add Expenses** — Log any expense with a description, amount, category, and date
- **Delete Expenses** — Remove individual entries instantly
- **Filter by Category** — View spending for a specific category or all at once
- **Sort Options** — Sort by newest, oldest, highest, or lowest amount
- **Dashboard Stats** — See total spending, number of entries, average per entry, and top spending category
- **Daily Spending Chart** — Line chart showing spending trends over time
- **Category Breakdown** — Visual summary of spending grouped by category
- **Persistent Storage** — All data saved to a local `expenses.json` file

---

## 🗂️ Project Structure

```
Eman_proj/
├── expense_tracker.py   # Flask backend — OOP models + REST API routes
├── requirements.txt     # Python dependencies
├── expenses.json        # Auto-generated data file (created on first run)
└── templates/
    └── index.html       # Frontend UI (HTML + CSS + JS)
```

---

## 🧠 Concepts Demonstrated

This project was built to demonstrate core Python and web development concepts:

| Concept | Where Used |
|---|---|
| **OOP (Classes)** | `Expense` and `ExpenseManager` classes |
| **Dictionaries** | Category summaries, JSON data, stats |
| **Lists** | Storing and filtering expense records |
| **Functions** | Route handlers and helper methods |
| **Exception Handling** | File I/O errors, invalid input validation |
| **File Handling** | Reading/writing `expenses.json` |
| **Flask (Web)** | Serves the HTML template + REST API |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Abdul-Rafay2005/Eman_proj.git
   cd Eman_proj
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app**
   ```bash
   python expense_tracker.py
   ```

4. **Open in your browser**
   ```
   http://127.0.0.1:5000
   ```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Serves the main UI |
| `GET` | `/api/expenses` | Get all expenses (supports `?category=` and `?sort=`) |
| `POST` | `/api/expenses` | Add a new expense |
| `DELETE` | `/api/expenses/<id>` | Delete an expense by ID |
| `GET` | `/api/stats` | Get dashboard statistics |

### Example — Add an Expense

```json
POST /api/expenses
{
  "description": "Lunch at work",
  "amount": 350,
  "category": "Food",
  "date": "2025-05-20"
}
```

---

## 📦 Dependencies

- [Flask](https://flask.palletsprojects.com/) `>=2.3.0`

---

## 📋 Expense Categories

Food · Transport · Shopping · Health · Education · Utilities · Entertainment · Other

---

## 👤 Author

**EMAN AHMED**
