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
