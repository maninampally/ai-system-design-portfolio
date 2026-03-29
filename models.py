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
    """Scaffold for the menu collection and category filtering.

    Category rule:
    - Categories are normalized when items are added to the catalog.
    - All filtering/search behavior assumes stored categories are canonical.
    """

    items: List[MenuItem] = field(default_factory=list)
    category_aliases: Dict[str, str] = field(
        default_factory=lambda: {
            "main": "main",
            "entree": "main",
            "main course": "main",
            "side": "side",
            "drink": "drink",
            "beverage": "drink",
            "dessert": "dessert",
            "desserts": "dessert",
        }
    )

    def add_item(self, item: MenuItem) -> None:
        """Add a MenuItem to the catalog.

        The item's category is normalized on insert so catalog data stays
        consistent for filtering.
        """
        item.category = self.normalize_category(item.category)
        self.items.append(item)

    def find_item(self, item_id: str) -> MenuItem:
        """Find a MenuItem by id.

        Raises:
            KeyError: If no item exists with the provided item_id.
        """
        for item in self.items:
            if item.item_id == item_id:
                return item
        raise KeyError(f"No menu item found for id '{item_id}'.")

    def filter_by_category(self, category: str) -> List[MenuItem]:
        """Return items in a category."""
        normalized = self.normalize_category(category)
        return [item for item in self.items if item.category == normalized]

    def sort_by_price(self, descending: bool = False) -> List[MenuItem]:
        """Return items sorted by price."""
        return sorted(self.items, key=lambda item: item.price, reverse=descending)

    def sort_by_popularity(self, descending: bool = True) -> List[MenuItem]:
        """Return items sorted by popularity rating."""
        return sorted(
            self.items,
            key=lambda item: item.popularity_rating,
            reverse=descending,
        )

    def normalize_category(self, raw: str) -> str:
        """Normalize inconsistent category labels.

        Raises:
            ValueError: If category is unknown or not supported.
        """
        key = raw.strip().lower()
        normalized = self.category_aliases.get(key)
        if normalized is None:
            raise ValueError(
                f"Unknown category '{raw}'. Supported values are: "
                f"{', '.join(sorted(self.category_aliases.keys()))}."
            )
        return normalized


@dataclass
class Customer:
    """Scaffold for a customer with purchase history."""

    customer_id: str
    name: str
    purchase_history: List["Order"] = field(default_factory=list)

    def add_order(self, order: "Order") -> None:
        """Add an order to purchase history."""
        self.purchase_history.append(order)

    def get_all_orders(self) -> List["Order"]:
        """Return all orders for the customer.

        Returns a copy to prevent external mutation of internal state.
        """
        return list(self.purchase_history)


@dataclass
class Order:
    """Scaffold for a customer transaction."""

    order_id: str
    customer_id: str
    items: List[MenuItem] = field(default_factory=list)

    def add_item(self, item: MenuItem) -> None:
        """Add an item to this order."""
        self.items.append(item)

    def remove_item(self, item_id: str) -> None:
        """Remove all matching items from this order by id.

        If duplicate items exist, all entries with that id are removed.
        """
        self.items = [item for item in self.items if item.item_id != item_id]

    def compute_total(self) -> float:
        """Compute order total cost."""
        return round(sum(item.price for item in self.items), 2)
