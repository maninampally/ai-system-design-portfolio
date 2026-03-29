import unittest

from models import Customer, MenuCatalog, MenuItem, Order


class BaseByteBitesTestCase(unittest.TestCase):
	def setUp(self) -> None:
		self.burger = MenuItem("m1", "Spicy Burger", 9.99, "Entree", 4.8)
		self.soda = MenuItem("m2", "Large Soda", 2.50, "Drink", 4.1)
		self.cake = MenuItem("m3", "Chocolate Cake", 5.25, "Desserts", 4.7)
		self.fries = MenuItem("m4", "Fries", 3.333, "Side", 4.3)

		self.catalog = MenuCatalog()
		self.catalog.add_item(self.burger)
		self.catalog.add_item(self.soda)
		self.catalog.add_item(self.cake)
		self.catalog.add_item(self.fries)


class TestCategoryFiltering(BaseByteBitesTestCase):
	def test_find_item_returns_correct_item(self) -> None:
		result = self.catalog.find_item("m1")
		self.assertEqual(result.name, "Spicy Burger")

	def test_find_item_raises_key_error_for_unknown_id(self) -> None:
		with self.assertRaises(KeyError):
			self.catalog.find_item("does-not-exist")

	def test_filter_drink_with_canonical_label(self) -> None:
		results = self.catalog.filter_by_category("drink")
		self.assertEqual([item.item_id for item in results], ["m2"])

	def test_filter_drink_with_alias_label(self) -> None:
		results = self.catalog.filter_by_category("beverage")
		self.assertEqual([item.item_id for item in results], ["m2"])

	def test_filter_main_with_alias_label(self) -> None:
		results = self.catalog.filter_by_category("main course")
		self.assertEqual([item.item_id for item in results], ["m1"])

	def test_filter_dessert_with_plural_alias(self) -> None:
		results = self.catalog.filter_by_category("desserts")
		self.assertEqual([item.item_id for item in results], ["m3"])

	def test_filter_category_is_case_and_whitespace_tolerant(self) -> None:
		results = self.catalog.filter_by_category("  DRINK  ")
		self.assertEqual([item.item_id for item in results], ["m2"])

	def test_filter_unknown_category_raises_value_error(self) -> None:
		with self.assertRaises(ValueError):
			self.catalog.filter_by_category("sandwich")

	def test_items_are_normalized_on_insert(self) -> None:
		self.assertEqual(self.burger.category, "main")
		self.assertEqual(self.soda.category, "drink")
		self.assertEqual(self.cake.category, "dessert")
		self.assertEqual(self.fries.category, "side")


class TestSortingBehavior(BaseByteBitesTestCase):
	def test_sort_by_price_ascending(self) -> None:
		sorted_items = self.catalog.sort_by_price(descending=False)
		self.assertEqual(
			[item.item_id for item in sorted_items],
			["m2", "m4", "m3", "m1"],
		)

	def test_sort_by_price_descending(self) -> None:
		sorted_items = self.catalog.sort_by_price(descending=True)
		self.assertEqual(
			[item.item_id for item in sorted_items],
			["m1", "m3", "m4", "m2"],
		)

	def test_sort_by_popularity_descending_default(self) -> None:
		sorted_items = self.catalog.sort_by_popularity()
		self.assertEqual(
			[item.item_id for item in sorted_items],
			["m1", "m3", "m4", "m2"],
		)

	def test_sort_by_popularity_ascending(self) -> None:
		sorted_items = self.catalog.sort_by_popularity(descending=False)
		self.assertEqual(
			[item.item_id for item in sorted_items],
			["m2", "m4", "m3", "m1"],
		)

	def test_sorting_returns_new_lists_without_mutating_catalog_order(self) -> None:
		original_ids = [item.item_id for item in self.catalog.items]
		_ = self.catalog.sort_by_price()
		_ = self.catalog.sort_by_popularity()
		self.assertEqual([item.item_id for item in self.catalog.items], original_ids)

	def test_sorting_empty_catalog_returns_empty_list(self) -> None:
		empty_catalog = MenuCatalog()
		self.assertEqual(empty_catalog.sort_by_price(), [])
		self.assertEqual(empty_catalog.sort_by_popularity(), [])


class TestOrderTotalCalculation(BaseByteBitesTestCase):
	def setUp(self) -> None:
		super().setUp()
		self.order = Order("o1", "c1")

	def test_total_is_zero_for_empty_order(self) -> None:
		self.assertEqual(self.order.compute_total(), 0)

	def test_duplicate_items_are_both_counted(self) -> None:
		self.order.add_item(self.soda)
		self.order.add_item(self.soda)
		self.assertEqual(len(self.order.items), 2)

	def test_total_for_single_item(self) -> None:
		self.order.add_item(self.burger)
		self.assertEqual(self.order.compute_total(), 9.99)

	def test_total_for_multiple_items(self) -> None:
		self.order.add_item(self.burger)
		self.order.add_item(self.soda)
		self.order.add_item(self.cake)
		self.assertEqual(self.order.compute_total(), 17.74)

	def test_total_rounds_to_two_decimals(self) -> None:
		self.order.add_item(self.burger)
		self.order.add_item(self.fries)
		self.assertEqual(self.order.compute_total(), 13.32)

	def test_total_updates_after_removing_items(self) -> None:
		self.order.add_item(self.burger)
		self.order.add_item(self.soda)
		self.order.add_item(self.soda)
		self.assertEqual(self.order.compute_total(), 14.99)

		self.order.remove_item("m2")
		self.assertEqual(self.order.compute_total(), 9.99)

	def test_remove_item_no_match_keeps_total_unchanged(self) -> None:
		self.order.add_item(self.burger)
		before = self.order.compute_total()
		self.order.remove_item("does-not-exist")
		self.assertEqual(self.order.compute_total(), before)


class TestIntegrationFlow(BaseByteBitesTestCase):
	def test_get_all_orders_returns_copy_not_reference(self) -> None:
		customer = Customer("c1", "Alex")
		customer.add_order(Order("o1", "c1"))

		orders_copy = customer.get_all_orders()
		orders_copy.append(Order("o2", "c1"))

		self.assertEqual(len(customer.get_all_orders()), 1)

	def test_end_to_end_browse_select_and_total(self) -> None:
		customer = Customer("c1", "Alex")
		order = Order("o100", customer.customer_id)

		drinks = self.catalog.filter_by_category("beverage")
		mains = self.catalog.filter_by_category("entree")
		desserts = self.catalog.filter_by_category("dessert")

		order.add_item(mains[0])
		order.add_item(drinks[0])
		order.add_item(desserts[0])

		customer.add_order(order)

		self.assertEqual(len(customer.get_all_orders()), 1)
		self.assertEqual(customer.get_all_orders()[0].compute_total(), 17.74)


if __name__ == "__main__":
	unittest.main(verbosity=2)