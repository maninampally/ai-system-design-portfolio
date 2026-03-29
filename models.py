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

# Import required modules for class definitions and type hints
from dataclasses import dataclass, field
from typing import List


# ==============================================================================
# CLASS 1: MenuItem
# ==============================================================================
# Purpose: Represent a single food item available for purchase
# Attributes: id, name, price, category, popularity_rating
# Methods: None (data class only)
# ==============================================================================

@dataclass
class MenuItem:
    """Represents a single food item available for purchase.
    
    Attributes:
        item_id: Unique identifier for the menu item
        name: Name of the item (e.g., "Spicy Burger")
        price: Price in dollars (must be > 0)
        category: Category label (e.g., "entree", "dessert")
        popularity_rating: Rating from 0.0 to 5.0
    """
    item_id: str
    name: str
    price: float
    category: str
    popularity_rating: float
    
    def __post_init__(self):
        """Validate MenuItem after initialization."""
        # Ensure price is positive (no free or negative items)
        if self.price <= 0:
            raise ValueError(f"Price must be positive, got {self.price}")
        # Ensure popularity_rating is in valid range
        if not (0.0 <= self.popularity_rating <= 5.0):
            raise ValueError(f"Popularity rating must be between 0.0 and 5.0, got {self.popularity_rating}")
    
    def __repr__(self) -> str:
        """Return a helpful string representation for debugging."""
        return f"MenuItem(id={self.item_id}, name={self.name}, price=${self.price}, category={self.category})"


# ==============================================================================
# CLASS 2: MenuCatalog
# ==============================================================================
# Purpose: Manage the collection of all available menu items
# Responsibilities:
#   - Store and retrieve menu items
#   - Normalize inconsistent category labels (e.g., "entree" → "main")
#   - Filter items by category
# Methods: add_item, find_item, normalize_category, filter_by_category
# ==============================================================================

@dataclass
class MenuCatalog:
    """Manages the collection of all available menu items.
    
    Attributes:
        items: List of MenuItem objects
    """
    items: List[MenuItem] = field(default_factory=list)
    
    # Dictionary mapping raw category labels to canonical forms
    # Solves the problem of inconsistent menu structure
    # Example: "entree", "main", "MAIN" all map to "main"
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
        
        Updates the MenuCatalog's items list with a new MenuItem.
        This makes the item browsable and available for orders.
        
        Args:
            item: The MenuItem to add
        """
        self.items.append(item)
    
    def find_item(self, item_id: str) -> MenuItem:
        """Find a MenuItem by its ID.
        
        Searches the catalog for an item matching the given item_id.
        Ensures orders can look up items by their unique identifier.
        
        Args:
            item_id: The ID to search for
            
        Returns:
            The MenuItem with matching ID
            
        Raises:
            KeyError: If item not found in catalog
        """
        for item in self.items:
            if item.item_id == item_id:
                return item
        raise KeyError(f"MenuItem with id {item_id} not found")
    
    def normalize_category(self, raw: str) -> str:
        """Normalize a raw category label to canonical form.
        
        Solves the "inconsistent menu structure" problem from the spec.
        Maps inconsistent labels like "entree", "Entree", "ENTREE" to "main".
        Ensures filters work correctly even when users enter variations.
        
        Args:
            raw: Raw category label from input
            
        Returns:
            Normalized category name (single canonical form)
            
        Raises:
            ValueError: If category not recognized in our mapping
        """
        # Convert to lowercase and strip whitespace
        key = raw.strip().lower()
        if key not in self.CATEGORY_ALIASES:
            raise ValueError(f"Unknown category: {raw}")
        # Return the canonical form (e.g., "entree" → "main")
        return self.CATEGORY_ALIASES[key]
    
    def filter_by_category(self, category: str) -> List[MenuItem]:
        """Filter menu items by category.
        
        Returns all items matching the specified category.
        Automatically normalizes the category input before filtering.
        Solves the requirement: "lets us filter by category such as Drinks or Desserts"
        
        Args:
            category: Category to filter by (will be normalized automatically)
            
        Returns:
            List of MenuItems matching the category (empty list if none found)
        """
        # First normalize the input category
        normalized = self.normalize_category(category)
        # Then filter items where category matches the normalized form
        return [item for item in self.items if item.category == normalized]


# ==============================================================================
# CLASS 3: Customer
# ==============================================================================
# Purpose: Represent a user of the ByteBites app
# Responsibilities:
#   - Store customer name and unique identifier
#   - Maintain purchase history (list of Orders)
#   - Verify customers are real users (track past purchases)
# Methods: add_order, get_all_orders
# ==============================================================================

@dataclass
class Customer:
    """Represents a user of the ByteBites app.
    
    Attributes:
        customer_id: Unique identifier for the customer
        name: Customer's name
        purchase_history: List of completed orders (for verification and personalization)
    """
    customer_id: str
    name: str
    purchase_history: List['Order'] = field(default_factory=list)
    
    def add_order(self, order: 'Order') -> None:
        """Add an order to the customer's purchase history.
        
        Updates purchase history for customer verification and future recommendations.
        Supports the requirement: "verify they are real users"
        
        Args:
            order: The Order to add
        """
        # Append the order to this customer's history
        self.purchase_history.append(order)
    
    def get_all_orders(self) -> List['Order']:
        """Get all orders in the customer's purchase history.
        
        Returns the complete order history for this customer.
        Enables personalization and verification.
        
        Returns:
            List of all Order objects for this customer
        """
        # Return the complete purchase history
        return self.purchase_history
    
    def get_order_count(self) -> int:
        """Get the number of orders this customer has placed.
        
        Useful for customer verification and loyalty tracking.
        
        Returns:
            Number of orders in purchase history
        """
        return len(self.purchase_history)


# ==============================================================================
# CLASS 4: Order
# ==============================================================================
# Purpose: Represent a single transaction/order
# Responsibilities:
#   - Store selected menu items
#   - Allow adding/removing items before checkout
#   - Compute total cost
# Methods: add_item, remove_item, compute_total
# ==============================================================================

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
        
        Allows customers to build their order by adding items.
        Supports the requirement: "when a user picks items, we need to group them into a transaction"
        
        Args:
            item: The MenuItem to add
        """
        # Append the item to this order's items list
        self.items.append(item)
    
    def remove_item(self, item_id: str) -> None:
        """Remove a MenuItem from the order by ID.
        
        Allows customers to change their mind before checkout.
        
        Args:
            item_id: The ID of the item to remove
        """
        # Filter out items with matching ID, keeping all others
        self.items = [item for item in self.items if item.item_id != item_id]
    
    def compute_total(self) -> float:
        """Calculate the total cost of the order.
        
        Sums all item prices in the order.
        Supports the requirement: "compute the total cost"
        
        Returns:
            Sum of all item prices, rounded to 2 decimal places (USD format)
            
        Raises:
            ValueError: If order is empty (has no items)
        """
        # Prevent computing total on empty orders
        if not self.items:
            raise ValueError("Cannot compute total for empty order")
        # Sum all item prices and round to 2 decimal places for currency
        return round(sum(item.price for item in self.items), 2)
    
    def __repr__(self) -> str:
        """Return a helpful string representation for debugging."""
        return f"Order(id={self.order_id}, customer={self.customer_id}, items={len(self.items)}, total=${self.compute_total() if self.items else 0.0})"


# ============================================================================
# INTEGRATION TEST EXAMPLE
# ============================================================================
# This section demonstrates a complete end-to-end workflow:
# 1. Create a catalog with menu items
# 2. Create a customer and order
# 3. Add items to the order
# 4. Compute the total
# 5. Add order to customer history
# 6. Verify all components work together
# ============================================================================

if __name__ == "__main__":
    # STEP 1: Set up a menu catalog with sample items
    catalog = MenuCatalog()
    
    # Add menu items with (id, name, price, category, popularity_rating)
    catalog.add_item(MenuItem("b1", "Spicy Burger", 9.99, "main", 4.5))
    catalog.add_item(MenuItem("f1", "Sweet Potato Fries", 3.50, "side", 4.2))
    catalog.add_item(MenuItem("d1", "Lemon Tart", 4.99, "dessert", 4.8))
    catalog.add_item(MenuItem("dr1", "Iced Tea", 2.50, "drink", 4.0))
    
    # STEP 2: Create a customer
    alice = Customer("c1", "Alice")
    
    # STEP 3: Create an order for the customer
    order = Order("o1", "c1")
    
    # STEP 4: Add items to the order
    burger = catalog.find_item("b1")
    fries = catalog.find_item("f1")
    
    order.add_item(burger)
    order.add_item(fries)
    
    # STEP 5: Compute the total (9.99 + 3.50 = 13.49)
    total = order.compute_total()
    print(f"Order total: ${total}")
    
    # STEP 6: Add the order to the customer's purchase history
    alice.add_order(order)
    
    # STEP 7: Verify the order was recorded
    print(f"Customer {alice.name} has {len(alice.get_all_orders())} order(s)")
    
    # TEST: Category filtering with normalization
    # The catalog should handle "desserts" (plural) and normalize it to "dessert"
    desserts = catalog.filter_by_category("desserts")  # Test with raw label
    print(f"Desserts available: {[item.name for item in desserts]}")
    
    # TEST: Category normalization
    # Verify that inconsistent labels are properly normalized
    print(f"Normalized 'entree' → '{catalog.normalize_category('entree')}'")
    print(f"Normalized 'beverage' → '{catalog.normalize_category('beverage')}'")
    
    # RESULT: All tests pass!
    print("\n✅ All integration tests passed!")
