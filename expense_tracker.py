"""
============================================================
  XPNS — Expense Tracker (Flask Web App)
============================================================
  Python backend for the cinematic expense tracker UI.

  Concepts Used:
  - Dictionaries       : category summaries, JSON data
  - Lists              : storing expense records
  - Functions          : logical route handlers & helpers
  - Exception Handling : try-except for file I/O & input
  - File Handling      : reading/writing expenses.json
  - OOP                : Expense, ExpenseManager classes
  - Web (Flask)        : serves HTML template + REST API
============================================================
  HOW TO RUN:
    python expense_tracker.py
  Then open: http://127.0.0.1:5000
============================================================
"""

# ── Standard Library ──────────────────────────────────────
import json
import os
from datetime import datetime

# ── Third-Party ───────────────────────────────────────────
from flask import Flask, render_template, request, jsonify, abort

# ── Global Constants ──────────────────────────────────────
DATA_FILE = "expenses.json"
CATEGORIES = [
    "Food", "Transport", "Shopping", "Health",
    "Education", "Utilities", "Entertainment", "Other"
]


# =============================================================
#  CLASS 1: Expense
#  Represents a single expense record (one row of data).
#  Concept: OOP — encapsulates data + behavior together.
# =============================================================
class Expense:
    """Represents a single expense entry."""

    def __init__(self, description: str, amount: float, category: str,
                 date: str = None, expense_id: int = None):
        self.expense_id  = expense_id or int(datetime.now().timestamp() * 1000)
        self.description = description.strip()
        self.amount      = float(amount)
        self.category    = category
        # Default to today's date if none provided
        self.date = date or datetime.today().strftime("%Y-%m-%d")

    # ── Convert object → dict (for JSON saving) ───────────
    def to_dict(self) -> dict:
        """CONCEPT: Dictionary — key-value pairs to store expense data."""
        return {
            "id":          self.expense_id,
            "description": self.description,
            "amount":      self.amount,
            "category":    self.category,
            "date":        self.date,
        }

    # ── Convert dict → object (for JSON loading) ──────────
    @staticmethod
    def from_dict(data: dict) -> "Expense":
        """Reconstructs an Expense object from a dictionary."""
        return Expense(
            description = data["description"],
            amount      = data["amount"],
            category    = data["category"],
            date        = data["date"],
            expense_id  = data.get("id"),
        )

    def __str__(self) -> str:
        return f"{self.date} | {self.category} | {self.description} | Rs {self.amount:.2f}"

    def __repr__(self) -> str:
        return f"Expense({self.description!r}, {self.amount}, {self.category!r})"


# =============================================================
#  CLASS 2: ExpenseManager
#  Manages the full list of expenses + file I/O operations.
#  Concepts: Lists, Dictionaries, File Handling, Exception Handling
# =============================================================
class ExpenseManager:
    """Manages expense data: storage, retrieval, and summaries."""

    def __init__(self, filepath: str = DATA_FILE):
        self.filepath = filepath
        self.expenses: list = []     # CONCEPT: List — all Expense objects
        self._load_from_file()

    # ────────────────────────────────────────────
    #  FILE HANDLING: Load expenses from JSON
    # ────────────────────────────────────────────
    def _load_from_file(self):
        """
        FILE HANDLING: Reads expenses.json into self.expenses.
        EXCEPTION HANDLING: Handles missing file, corrupt JSON, bad keys.
        """
        try:
            if os.path.exists(self.filepath):
                with open(self.filepath, "r", encoding="utf-8") as f:
                    raw = json.load(f)            # Parse JSON → Python list
                    # CONCEPT: List comprehension — build Expense objects
                    self.expenses = [Expense.from_dict(d) for d in raw]
        except json.JSONDecodeError as e:
            print(f"[ERROR] Could not parse {self.filepath}: {e}")
            self.expenses = []
        except KeyError as e:
            print(f"[ERROR] Missing field in data: {e}")
            self.expenses = []
        except IOError as e:
            print(f"[ERROR] Could not read file: {e}")
            self.expenses = []

    # ────────────────────────────────────────────
    #  FILE HANDLING: Save expenses to JSON
    # ────────────────────────────────────────────
    def _save_to_file(self):
        """
        FILE HANDLING: Writes all expenses to expenses.json.
        EXCEPTION HANDLING: Catches disk / permission errors.
        """
        try:
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(
                    [exp.to_dict() for exp in self.expenses],  # CONCEPT: List → list of dicts
                    f,
                    indent=4,
                    ensure_ascii=False
                )
        except IOError as e:
            print(f"[ERROR] Could not save data: {e}")
            raise  # Re-raise so API route can return 500

    # ────────────────────────────────────────────
    #  FUNCTION: Add a new expense
    # ────────────────────────────────────────────
    def add_expense(self, description: str, amount, category: str, date: str) -> Expense:
        """
        Validates inputs, creates Expense, appends to list, saves.
        EXCEPTION HANDLING: Raises ValueError on bad input.
        Returns the created Expense object.
        """
        if not description or not description.strip():
            raise ValueError("Description cannot be empty.")

        try:
            amount = float(amount)
        except (TypeError, ValueError):
            raise ValueError(f"Invalid amount: '{amount}'. Must be a number.")

        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")

        if category not in CATEGORIES:
            raise ValueError(f"Invalid category: '{category}'.")

        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format.")

        expense = Expense(description, amount, category, date)
        self.expenses.append(expense)    # CONCEPT: List — append
        self._save_to_file()
        return expense

    # ────────────────────────────────────────────
    #  FUNCTION: Delete expense by ID
    # ────────────────────────────────────────────
    def delete_expense(self, expense_id: int) -> bool:
        """
        Removes the expense with the given ID from the list.
        EXCEPTION HANDLING: Returns False if ID not found.
        """
        original_count = len(self.expenses)
        # CONCEPT: List comprehension — filter out the deleted item
        self.expenses = [e for e in self.expenses if e.expense_id != expense_id]

        if len(self.expenses) == original_count:
            return False   # Nothing was removed

        self._save_to_file()
        return True

    # ────────────────────────────────────────────
    #  FUNCTION: Get all expenses (as dicts)
    # ────────────────────────────────────────────
    def get_all(self) -> list:
        """Returns all expenses as a list of dictionaries."""
        # CONCEPT: List — iterate and convert each object
        return [e.to_dict() for e in self.expenses]

    # ────────────────────────────────────────────
    #  FUNCTION: Filter by category
    # ────────────────────────────────────────────
    def filter_by_category(self, category: str) -> list:
        """
        CONCEPT: List — returns filtered subset by category.
        Returns all if category is 'All'.
        """
        if category == "All":
            return self.get_all()
        return [e.to_dict() for e in self.expenses if e.category == category]

    # ────────────────────────────────────────────
    #  FUNCTION: Get total spending
    # ────────────────────────────────────────────
    def get_total(self) -> float:
        """CONCEPT: List — sums all expense amounts."""
        return sum(e.amount for e in self.expenses)

    # ────────────────────────────────────────────
    #  FUNCTION: Category summary (Dictionary)
    # ────────────────────────────────────────────
    def get_summary_by_category(self) -> dict:
        """
        CONCEPT: Dictionary — groups total spending per category.
        Returns: { "Food": 1500.0, "Transport": 300.0, ... }
        """
        summary = {}   # Empty dict to accumulate totals
        for exp in self.expenses:
            # If key exists, add to it; otherwise start from 0
            summary[exp.category] = summary.get(exp.category, 0) + exp.amount
        return summary   # CONCEPT: Dictionary

    # ────────────────────────────────────────────
    #  FUNCTION: Summary statistics
    # ────────────────────────────────────────────
    def get_daily_spending(self) -> dict:
        """
        CONCEPT: Dictionary — groups total spending per date.
        Returns: { "2025-05-01": 450.0, "2025-05-02": 200.0, ... }
        Used to populate the line chart on the dashboard.
        """
        daily = {}
        for exp in self.expenses:
            daily[exp.date] = round(daily.get(exp.date, 0) + exp.amount, 2)
        return daily   # CONCEPT: Dictionary

    def get_stats(self) -> dict:
        """
        Returns a dictionary of key stats for the dashboard.
        CONCEPT: Dictionary — aggregated data for the UI.
        """
        total   = self.get_total()
        count   = len(self.expenses)
        average = round(total / count, 2) if count else 0.0
        summary = self.get_summary_by_category()
        daily   = self.get_daily_spending()

        # CONCEPT: Dictionary — find the category with max spending
        top_category = max(summary, key=summary.get) if summary else None

        return {
            "total":        round(total, 2),
            "count":        count,
            "average":      average,
            "top_category": top_category,
            "summary":      summary,
            "daily":        daily,
        }


# =============================================================
#  FLASK APPLICATION
#  Routes act as the "controller" layer between the
#  ExpenseManager (model) and the HTML template (view).
# =============================================================
app = Flask(__name__)

# One shared manager instance for the app lifetime
manager = ExpenseManager()


# ── ROUTE: Main Page ──────────────────────────────────────
@app.route("/")
def index():
    """Serves the main HTML template (the cinematic UI)."""
    return render_template("index.html", categories=CATEGORIES)


# ── API: Get all expenses ─────────────────────────────────
@app.route("/api/expenses", methods=["GET"])
def api_get_expenses():
    """
    Returns filtered + sorted expenses as JSON.
    Query params: category, sort
    """
    category = request.args.get("category", "All")
    sort_by  = request.args.get("sort", "newest")

    try:
        expenses = manager.filter_by_category(category)

        # CONCEPT: Dictionary — each expense is a dict; sort by its fields
        if sort_by == "newest":
            expenses.sort(key=lambda x: (x["date"], x["id"]), reverse=True)
        elif sort_by == "oldest":
            expenses.sort(key=lambda x: (x["date"], x["id"]))
        elif sort_by == "highest":
            expenses.sort(key=lambda x: x["amount"], reverse=True)
        elif sort_by == "lowest":
            expenses.sort(key=lambda x: x["amount"])

        # Filtered total
        total = sum(e["amount"] for e in expenses)

        return jsonify({
            "success":  True,
            "expenses": expenses,
            "total":    round(total, 2),
            "count":    len(expenses),
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ── API: Add expense ──────────────────────────────────────
@app.route("/api/expenses", methods=["POST"])
def api_add_expense():
    """
    Receives JSON body, validates, adds expense.
    EXCEPTION HANDLING: Returns 400 on bad input.
    """
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "error": "No data provided."}), 400

    try:
        expense = manager.add_expense(
            description = data.get("description", ""),
            amount      = data.get("amount"),
            category    = data.get("category", "Other"),
            date        = data.get("date", datetime.today().strftime("%Y-%m-%d")),
        )
        return jsonify({"success": True, "expense": expense.to_dict()}), 201

    except ValueError as e:
        # EXCEPTION HANDLING: User sent invalid data
        return jsonify({"success": False, "error": str(e)}), 400
    except IOError as e:
        # EXCEPTION HANDLING: File could not be saved
        return jsonify({"success": False, "error": "Could not save data."}), 500


# ── API: Delete expense ───────────────────────────────────
@app.route("/api/expenses/<int:expense_id>", methods=["DELETE"])
def api_delete_expense(expense_id: int):
    """
    Deletes the expense with the given ID.
    EXCEPTION HANDLING: Returns 404 if not found.
    """
    try:
        deleted = manager.delete_expense(expense_id)
        if not deleted:
            return jsonify({"success": False, "error": "Expense not found."}), 404
        return jsonify({"success": True})
    except IOError:
        return jsonify({"success": False, "error": "Could not save after delete."}), 500


# ── API: Summary statistics ───────────────────────────────
@app.route("/api/stats", methods=["GET"])
def api_get_stats():
    """
    Returns dashboard stats: total, count, average, top category.
    CONCEPT: Dictionary — structured data returned as JSON.
    """
    try:
        stats = manager.get_stats()
        return jsonify({"success": True, **stats})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# =============================================================
#  ENTRY POINT
# =============================================================
def main():
    """Starts the Flask development server."""
    print("=" * 55)
    print("  XPNS — Expense Tracker")
    print("  Open in browser: http://127.0.0.1:5000")
    print("=" * 55)
    app.run(debug=True, port=5000)


if __name__ == "__main__":
    main()