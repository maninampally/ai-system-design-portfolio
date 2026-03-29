"""
ByteBites class scaffolds based on the approved UML diagram.

Core classes:
1. Customer
2. MenuItem
3. MenuCatalog
4. Order
"""

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class MenuItem:
    """Scaffold for a single menu item."""

    item_id: str
    name: str
    price: float
    category: str
    popularity_rating: float


@dataclass
class MenuCatalog:
    """Scaffold for the menu collection and category filtering."""

    items: List[MenuItem] = field(default_factory=list)
    category_aliases: Dict[str, str] = field(
        default_factory=lambda: {
            "entree": "main",
            "main course": "main",
            "beverage": "drink",
            "desserts": "dessert",
        }
    )

    def add_item(self, item: MenuItem) -> None:
        """Add a MenuItem to the catalog."""
        pass

    def find_item(self, item_id: str) -> MenuItem:
        """Find a MenuItem by id."""
        pass

    def filter_by_category(self, category: str) -> List[MenuItem]:
        """Return items in a category."""
        pass

    def normalize_category(self, raw: str) -> str:
        """Normalize inconsistent category labels."""
        pass


@dataclass
class Customer:
    """Scaffold for a customer with purchase history."""

    customer_id: str
    name: str
    purchase_history: List["Order"] = field(default_factory=list)

    def add_order(self, order: "Order") -> None:
        """Add an order to purchase history."""
        pass

    def get_all_orders(self) -> List["Order"]:
        """Return all orders for the customer."""
        pass


@dataclass
class Order:
    """Scaffold for a customer transaction."""

    order_id: str
    customer_id: str
    items: List[MenuItem] = field(default_factory=list)

    def add_item(self, item: MenuItem) -> None:
        """Add an item to this order."""
        pass

    def remove_item(self, item_id: str) -> None:
        """Remove an item from this order by id."""
        pass

    def compute_total(self) -> float:
        """Compute order total cost."""
        pass
