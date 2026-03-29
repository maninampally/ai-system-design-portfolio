# ByteBites: AI-Assisted System Design Portfolio

## Overview

**ByteBites** is a backend system for a food delivery application built as a hands-on portfolio project. It demonstrates complete system design workflow: gathering requirements, architecting solutions, implementing code, and validating with comprehensive tests—**all guided by AI as a thinking partner**.

This project showcases real-world practices in requirements breakdown, UML design, Python implementation, automated testing, and version control.

**Status:** ✅ Production-Ready MVP (24/24 tests passing)  
**Built:** March 2026  
**Duration:** Complete system design cycle in one workflow

---

## WHAT is ByteBites?

A **backend data model** for a food delivery app that handles:

- 🧑 **Customer Management**: Track users and their order history
- 🍔 **Menu Items**: Store food products with pricing and ratings
- 📋 **Menu Catalog**: Searchable collection with filtering and sorting
- 🛒 **Order Processing**: Group items and compute transaction totals

**Core Classes:**
- `MenuItem`: Food item data (name, price, category, rating)
- `MenuCatalog`: Menu collection with filter/sort operations
- `Order`: Shopping transaction with item management
- `Customer`: User profile with purchase history

---

## WHY We Built It

**Learning Goal:** Demonstrate AI-assisted system design from first principles
- How to translate client requests into class structures
- How to design for extensibility and error handling
- How to test comprehensively without external dependencies
- How to use AI as a collaborative thinking partner

**Real-World Relevance:** Every mobile app backend needs:
- Consistent data management (category normalization)
- Defensive coding practices (copy semantics)
- Precision in calculations (currency rounding)
- Comprehensive validation (24 test cases)

---

## HOW It Works

### Quick Start

#### 1. Run the Tests (Verify Everything Works)
```bash
python -m unittest test_bytebites.py -v
```
**Expected Output:**
```
Ran 24 tests in 0.006s
OK
```

#### 2. Explore the Code
```python
from models import Customer, MenuCatalog, MenuItem, Order

# Create menu items
burger = MenuItem("m1", "Spicy Burger", 9.99, "Entree", 4.8)
soda = MenuItem("m2", "Large Soda", 2.50, "Drink", 4.1)

# Build catalog
catalog = MenuCatalog()
catalog.add_item(burger)
catalog.add_item(soda)

# Filter by category (alias works: "beverage" → "drink")
drinks = catalog.filter_by_category("beverage")  # Returns [soda]

# Create order
order = Order("o1", "c1")
order.add_item(burger)
order.add_item(soda)

# Compute total (handles rounding)
total = order.compute_total()  # Returns 12.49

# Track customer history
customer = Customer("c1", "Alex")
customer.add_order(order)
all_orders = customer.get_all_orders()  # Returns defensive copy
```

#### 3. Key Features Demonstrated

| Feature | Example | Why It Matters |
|---|---|---|
| **Category Normalization** | "beverage" → "drink" | Handles inconsistent user input |
| **Defensive Copies** | `get_all_orders()` returns copy | Prevents accidental state corruption |
| **Rounding Precision** | 9.99 + 3.333 = 13.32 | Accurate currency handling |
| **Error Handling** | `KeyError`, `ValueError` | Clear failure modes |
| **Non-Mutating Sorts** | `sort_by_price()` returns new list | Original catalog unchanged |

---

## Project Structure

```
ai-system-design-portfolio/
├── models.py                      # Core implementation (163 lines, 4 classes)
├── test_bytebites.py              # Test suite (24 tests, 100% passing)
├── PROJECT_DOCUMENTATION.md       # Detailed system documentation
├── README.md                       # This file
├── bytebites_spec.md              # Client feature request
├── bytebites_design.md            # UML architecture diagram
├── TEST_VALIDATION_SUMMARY.md     # Test coverage breakdown
└── .gitignore                     # Git ignore rules
```

---

## Design Highlights

### 1. Category Alias System
Instead of hardcoding filters, normalize categories on insert:
```python
category_aliases = {
    "entree": "main",
    "beverage": "drink",
    "desserts": "dessert",
}
```
✅ **Benefit:** Catalog stays consistent; filtering is reliable

### 2. Defensive Copy Pattern
Public methods return copies, not references:
```python
def get_all_orders(self) -> List[Order]:
    return list(self.purchase_history)  # Copy, not reference
```
✅ **Benefit:** External code can't accidentally mutate internal state

### 3. Non-Mutating Sorting
Use `sorted()` instead of `sort()`:
```python
def sort_by_price(self, descending: bool = False):
    return sorted(self.items, key=lambda item: item.price, reverse=descending)
```
✅ **Benefit:** Caller can sort without modifying original catalog

### 4. Precision Rounding
Compute totals with proper decimal handling:
```python
def compute_total(self) -> float:
    return round(sum(item.price for item in self.items), 2)
```
✅ **Benefit:** Accurate currency (9.99 + 3.333 ≠ 13.323...)

---

## Test Coverage (24 Tests, 100% Passing)

### Category Filtering & Lookup (9 tests)
- ✅ Find item by ID
- ✅ Handle missing items (KeyError)
- ✅ Filter by canonical labels (drink)
- ✅ Filter by aliases (beverage → drink)
- ✅ Handle case/whitespace (  DRINK  )
- ✅ Reject unknown categories (ValueError)
- ✅ Normalize on insert

### Sorting Behavior (6 tests)
- ✅ Sort price ascending/descending
- ✅ Sort popularity ascending/descending
- ✅ Don't mutate original catalog
- ✅ Handle empty catalog

### Order Total Calculation (9 tests)
- ✅ Empty order = $0.00
- ✅ Single item = item price
- ✅ Multiple items = sum
- ✅ Rounding precision (2 decimals)
- ✅ Duplicate items counted correctly
- ✅ Removal updates total
- ✅ Missing ID removal is no-op

### Integration & Safety (3 tests)
- ✅ End-to-end browse → select → order → total
- ✅ Defensive copy prevents mutation
- ✅ Customer history isolation

**Run Tests:**
```bash
python -m unittest test_bytebites.py -v
```

---

## How to Extend

### Add a New Category Alias
```python
# In models.py, MenuCatalog.category_aliases
"appetizer": "appetizer",
```

### Add a New Sorting Method
```python
def sort_by_rating(self, descending: bool = True) -> List[MenuItem]:
    return sorted(
        self.items,
        key=lambda item: item.popularity_rating,
        reverse=descending,
    )
```

### Add a New Order Method
```python
def get_item_count(self) -> int:
    return len(self.items)

def has_item(self, item_id: str) -> bool:
    return any(item.item_id == item_id for item in self.items)
```

**Remember:** Add tests for every new feature!

---

## Key Decisions & Rationale

| Decision | Reason |
|---|---|
| Use @dataclass | Auto-generated `__init__`, clean type hints |
| Store items as list | Allows duplicates; simpler than dictionary |
| Normalize on insert | Ensures catalog consistency |
| Return copies | Prevents accidental mutation |
| Sort returns new list | Non-destructive; catalog unchanged |
| Round to 2 decimals | Currency precision |
| Raise exceptions | Clear failure modes |

---

## Git & Version Control

**Commits:**
```
3d1f4fb - Add .gitignore for Python cache
20f467e - Update test suite with complete validation
69140e5 - Add validated tests: 24 unit tests
99bcd1e - Create test file
```

**How to View History:**
```bash
git log --oneline
```

---

## Next Steps & Future Enhancements

### Phase 2 (Optional Extensions)
- [ ] Add database layer (SQLite/PostgreSQL)
- [ ] REST API wrapper (Flask/FastAPI)
- [ ] Payment processing integration
- [ ] Inventory management
- [ ] AI recommendation engine
- [ ] Order tracking (pending → shipped → delivered)
- [ ] Analytics & reporting

---

## Learning Outcomes

By building ByteBites, you'll understand:

1. **System Design** — How to architect multi-class systems
2. **Python Best Practices** — Type hints, dataclasses, defensive coding
3. **Testing Mindset** — What to test, why, and how (24 test patterns)
4. **Error Handling** — Raising meaningful exceptions
5. **Version Control** — Commit discipline and history
6. **AI Collaboration** — Using AI as a thinking partner, not just code generator

---

## Resources & Links

- **Full Documentation:** See `PROJECT_DOCUMENTATION.md` for detailed architecture, design rationale, and complete code listings
- **Test Details:** See `TEST_VALIDATION_SUMMARY.md` for test coverage overview
- **Architecture Diagram:** See `bytebites_design.md` for UML class relationships
- **Original Spec:** See `bytebites_spec.md` for client feature request

---

## License & Attribution

Portfolio project built during CodePath's AI workflows curriculum.  
Designed with AI as a thinking partner using iterative refinement.

---

**Questions?** Review `PROJECT_DOCUMENTATION.md` for complete system explanation.  
**Want to contribute?** Add tests first, then implement features.
