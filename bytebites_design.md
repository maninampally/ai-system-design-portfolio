# ByteBites Core Architecture Design

## Candidate Classes
1. Customer
2. MenuItem
3. MenuCatalog
4. Order

## UML-Style Class Diagram

~~~mermaid
classDiagram
direction LR

class Customer {
  +customer_id: str
  +name: str
  +purchase_history: List~Order~
  +add_order(order: Order): void
  +get_all_orders(): List~Order~
}

class MenuItem {
  +item_id: str
  +name: str
  +price: float
  +category: str
  +popularity_rating: float
}

class MenuCatalog {
  +items: List~MenuItem~
  +add_item(item: MenuItem): void
  +find_item(item_id: str): MenuItem
  +filter_by_category(category: str): List~MenuItem~
  +normalize_category(raw: str): str
}

class Order {
  +order_id: str
  +customer_id: str
  +items: List~MenuItem~
  +add_item(item: MenuItem): void
  +remove_item(item_id: str): void
  +compute_total(): float
}

Customer "1" --> "0..*" Order : places
Order "1" --> "1..*" MenuItem : contains
MenuCatalog "1" o-- "0..*" MenuItem : manages
~~~

## Design Considerations

### Alignment to Feature Request
1. **Customer management**: Tracks `name` and `purchase_history` to verify real users.
2. **MenuItem structure**: Stores `name`, `price`, `category`, and `popularity_rating` as requested.
3. **MenuCatalog**: Provides digital list with `filter_by_category()` functionality.
4. **Order**: Groups selected items and computes total cost via `compute_total()`.

### Key Design Decisions
1. **MenuCatalog.normalize_category()**: Handles inconsistent menu labels (e.g., "entree" → "main").
2. **MenuItem** attributes only: No methods beyond core properties to keep MVP lean.
3. **Order.items list**: Direct storage of MenuItem objects for simplicity.
4. **Relationships**: 1-to-many (Customer → Order, Order → MenuItem); 1-to-many (MenuCatalog → MenuItem).

### Future Enhancements (Out of Scope for MVP)
- Payment processing
- Delivery zone management
- AI recommendation engine
- Order status tracking (pending → confirmed → shipped)
- Inventory management
