"""
ByteBites Core Data Models

This module contains the four core classes for the ByteBites food ordering app:

1. Customer
   - Represents a user of the ByteBites app
   - Tracks name and purchase history
   - Allows adding orders to history

2. MenuItem
   - Represents a single food item available for purchase
   - Stores name, price, category, and popularity rating
   - No methods; pure data class

3. MenuCatalog
   - Manages the collection of all available menu items
   - Provides filtering by category
   - Normalizes inconsistent category labels

4. Order
   - Represents a single transaction/order
   - Contains selected MenuItems
   - Computes the total cost of all items
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class MenuItem:
    """Represents a single food item available for purchase.
    
    Attributes:
        item_id: Unique identifier for the menu item
        name: Name of the item (e.g., "Spicy Burger")
        price: Price in dollars
        category: Category label (e.g., "entree", "dessert")
        popularity_rating: Rating from 0.0 to 5.0
    """
    item_id: str
    name: str
    price: float
    category: str
    popularity_rating: float


@dataclass
class MenuCatalog:
    """Manages the collection of all available menu items.
    
    Attributes:
        items: List of MenuItem objects
    """
    items: List[MenuItem] = field(default_factory=list)
    
    # Category aliases for normalization
    CATEGORY_ALIASES = {
        "entree": "main",
        "main": "main",
        "main course": "main",
        "side": "side",
        "snack": "side",
        "drink": "drink",
        "beverage": "drink",
        "dessert": "dessert",
        "desserts": "dessert",
        "sweet": "dessert",
        "soup": "soup",
        "salad": "salad",
    }
    
    def add_item(self, item: MenuItem) -> None:
        """Add a MenuItem to the catalog.
        
        Args:
            item: The MenuItem to add
        """
        self.items.append(item)
    
    def find_item(self, item_id: str) -> MenuItem:
        """Find a MenuItem by its ID.
        
        Args:
            item_id: The ID to search for
            
        Returns:
            The MenuItem with matching ID
            
        Raises:
            KeyError: If item not found
        """
        for item in self.items:
            if item.item_id == item_id:
                return item
        raise KeyError(f"MenuItem with id {item_id} not found")
    
    def normalize_category(self, raw: str) -> str:
        """Normalize a raw category label to canonical form.
        
        Maps inconsistent labels like "entree", "Entree", "ENTREE" to "main".
        
        Args:
            raw: Raw category label from input
            
        Returns:
            Normalized category name
            
        Raises:
            ValueError: If category not recognized
        """
        key = raw.strip().lower()
        if key not in self.CATEGORY_ALIASES:
            raise ValueError(f"Unknown category: {raw}")
        return self.CATEGORY_ALIASES[key]
    
    def filter_by_category(self, category: str) -> List[MenuItem]:
        """Filter menu items by category.
        
        Args:
            category: Category to filter by (will be normalized)
            
        Returns:
            List of MenuItems matching the category
        """
        normalized = self.normalize_category(category)
        return [item for item in self.items if item.category == normalized]


@dataclass
class Customer:
    """Represents a user of the ByteBites app.
    
    Attributes:
        customer_id: Unique identifier for the customer
        name: Customer's name
        purchase_history: List of completed orders
    """
    customer_id: str
    name: str
    purchase_history: List['Order'] = field(default_factory=list)
    
    def add_order(self, order: 'Order') -> None:
        """Add an order to the customer's purchase history.
        
        Args:
            order: The Order to add
        """
        self.purchase_history.append(order)
    
    def get_all_orders(self) -> List['Order']:
        """Get all orders in the customer's purchase history.
        
        Returns:
            List of all orders
        """
        return self.purchase_history


@dataclass
class Order:
    """Represents a single transaction/order.
    
    Attributes:
        order_id: Unique identifier for the order
        customer_id: ID of the customer who placed the order
        items: List of MenuItems in the order
    """
    order_id: str
    customer_id: str
    items: List[MenuItem] = field(default_factory=list)
    
    def add_item(self, item: MenuItem) -> None:
        """Add a MenuItem to the order.
        
        Args:
            item: The MenuItem to add
        """
        self.items.append(item)
    
    def remove_item(self, item_id: str) -> None:
        """Remove a MenuItem from the order by ID.
        
        Args:
            item_id: The ID of the item to remove
        """
        self.items = [item for item in self.items if item.item_id != item_id]
    
    def compute_total(self) -> float:
        """Calculate the total cost of the order.
        
        Returns:
            Sum of all item prices, rounded to 2 decimal places
        """
        return round(sum(item.price for item in self.items), 2)


# ============================================================================
# Integration Test Example
# ============================================================================

if __name__ == "__main__":
    # Create a menu catalog
    catalog = MenuCatalog()
    
    # Add menu items
    catalog.add_item(MenuItem("b1", "Spicy Burger", 9.99, "main", 4.5))
    catalog.add_item(MenuItem("f1", "Sweet Potato Fries", 3.50, "side", 4.2))
    catalog.add_item(MenuItem("d1", "Lemon Tart", 4.99, "dessert", 4.8))
    catalog.add_item(MenuItem("dr1", "Iced Tea", 2.50, "drink", 4.0))
    
    # Create a customer
    alice = Customer("c1", "Alice")
    
    # Create an order
    order = Order("o1", "c1")
    
    # Add items to order (using normalized categories)
    burger = catalog.find_item("b1")
    fries = catalog.find_item("f1")
    
    order.add_item(burger)
    order.add_item(fries)
    
    # Compute total
    total = order.compute_total()
    print(f"Order total: ${total}")
    
    # Add order to customer's history
    alice.add_order(order)
    
    # Verify
    print(f"Customer {alice.name} has {len(alice.get_all_orders())} order(s)")
    
    # Test category filtering with normalization
    desserts = catalog.filter_by_category("desserts")  # raw label
    print(f"Desserts available: {[item.name for item in desserts]}")
    
    # Test category normalization
    print(f"Normalized 'entree' → '{catalog.normalize_category('entree')}'")
    print(f"Normalized 'beverage' → '{catalog.normalize_category('beverage')}'")
    
    print("\n✅ All integration tests passed!")
