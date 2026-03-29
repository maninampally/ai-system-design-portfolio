classDiagram
direction LR

class Customer {
  -customer_id: str
  -name: str
  -email: str
  -is_verified: bool
  -purchase_history: List~Order~
  -created_at: datetime

  +add_order(order: Order): None
  +get_order_count(): int
  +get_total_spent(): float
  +has_purchased_item(item_id: str): bool
  +verify_identity(min_orders: int = 1): bool
}

class MenuItem {
  -item_id: str
  -name: str
  -price: float
  -category: str
  -popularity_rating: float
  -is_available: bool
  -tags: Set~str~

  +update_price(new_price: float): None
  +update_popularity(delta: float): None
  +set_availability(flag: bool): None
  +matches_category(category: str): bool
  +is_affordable(max_price: float): bool
  +to_dict(): dict
}

class MenuCatalog {
  -items_by_id: Dict~str, MenuItem~
  -category_aliases: Dict~str, str~

  +normalize_category(raw_category: str): str
  +add_item(item: MenuItem): None
  +remove_item(item_id: str): bool
  +get_item(item_id: str): MenuItem
  +list_all_items(): List~MenuItem~
  +filter_by_category(category: str): List~MenuItem~
  +filter_by_price(min_price: float, max_price: float): List~MenuItem~
  +search_by_name(keyword: str): List~MenuItem~
  +sort_by_price(desc: bool = false): List~MenuItem~
  +top_popular(limit: int = 5): List~MenuItem~
}

class Order {
  -order_id: str
  -customer_id: str
  -items: List~MenuItem~
  -quantities: Dict~str, int~
  -status: str
  -created_at: datetime
  -updated_at: datetime
  -tax_rate: float

  +add_item(item: MenuItem, qty: int = 1): None
  +remove_item(item_id: str, qty: int = 1): None
  +set_quantity(item_id: str, qty: int): None
  +compute_subtotal(): float
  +compute_tax(): float
  +compute_total(): float
  +validate_against_catalog(catalog: MenuCatalog): bool
  +finalize(): bool
  +to_receipt_lines(): List~str~
}

Customer "1" --> "0..*" Order : places
Order "1" --> "1..*" MenuItem : contains
MenuCatalog "1" o-- "0..*" MenuItem : manages
Order ..> MenuCatalog : validates_with