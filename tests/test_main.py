import unittest
from src.phone_book import *
from src.birthdays import *


class TestAddressBook(unittest.TestCase):
    def setUp(self) -> None:
        self.book = AddressBook(load_from_file=False)
        self.error_msg = "Invalid command format."
        self.name = "ivan"
        self.phone = "1231231231"
        self.email = "ivan@gmail.com"
        self.address = "Odesa, Tiraspolska 11"
        return super().setUp()

    def test_add_contact(self):
        add_contact([self.name, self.phone], self.book)
        new_name = "olha"
        new_phone = "3213123111"
        add_contact([new_name, new_phone], self.book)
        self.assertEqual(len(self.book), 2)

    def test_remove_contact(self):
        add_contact([self.name, self.phone], self.book)
        remove_contact([self.name], self.book)
        self.assertEqual(len(self.book), 0)

    def test_contact_add_phone(self):
        add_contact([self.name, self.phone], self.book)
        add_contact([self.name, "3213213211"], self.book)
        self.assertEqual(len(self.book.data[self.name].phones), 2)

    def test_contact_remove_phone(self):
        add_contact([self.name, self.phone], self.book)
        new_phone = "3213213211"
        add_contact([self.name, new_phone], self.book)
        remove_contact([self.name, str(self.phone)], self.book)
        self.assertEqual(len(self.book.data[self.name].phones), 1)
        self.assertEqual(self.book.data[self.name].phones[0].value, new_phone)

    def test_contact_add_email(self):
        add_contact([self.name, self.phone], self.book)
        add_email([self.name, self.email], self.book)
        self.assertEqual(len(self.book.data[self.name].emails), 1)
        self.assertEqual(self.book.data[self.name].emails[0].value, self.email)

    def test_contact_remove_email(self):
        add_contact([self.name, self.phone], self.book)
        add_email([self.name, self.email], self.book)
        remove_contact([self.name, str(self.email)], self.book)
        self.assertEqual(len(self.book.data[self.name].emails), 0)

    def test_contact_add_address(self):
        add_contact([self.name, self.phone], self.book)
        add_address([self.name, self.address], self.book)
        self.assertEqual(len(self.book.data[self.name].address), 1)
        self.assertEqual(self.book.data[self.name].address[0].value, self.address)

    def test_contact_remove_address(self):
        add_contact([self.name, self.phone], self.book)
        add_email([self.name, self.email], self.book)
        remove_contact([self.name, str(self.address)], self.book)
        self.assertEqual(len(self.book.data[self.name].address), 0)

    def test_contact_change_phone(self):
        new_phone = "3213213121"
        changed_phone = "3213213199"
        add_contact([self.name, self.phone], self.book)
        add_contact([self.name, new_phone], self.book)
        change_contact([self.name, new_phone, changed_phone], self.book)
        self.assertEqual(len(self.book.data[self.name].phones), 2)
        collection = self.book.data[self.name].phones
        self.assertIsNotNone(
            self.book.data[self.name].find_item(changed_phone, collection).value
        )

    def test_contact_change_email(self):
        new_email = "foo@gmail.com"
        changed_email = "bar@gmail.com"
        add_contact([self.name, self.phone], self.book)
        add_email([self.name, new_email], self.book)
        change_contact([self.name, new_email, changed_email], self.book)
        self.assertEqual(len(self.book.data[self.name].emails), 1)
        collection = self.book.data[self.name].emails
        self.assertIsNotNone(
            self.book.data[self.name].find_item(changed_email, collection).value
        )

    def test_contact_change_address(self):
        new_address = "Odesa Tirasposka 12"
        changed_address = "Kyiv Lomonosava 8"
        add_contact([self.name, self.phone], self.book)
        add_address([self.name, new_address], self.book)
        result = change_contact(
            [self.name, new_address, "|", changed_address], self.book
        )
        self.assertEqual(
            result,
            f"{self.name}'s address '{new_address}' changed to '{changed_address}'.",
        )
        self.assertEqual(len(self.book.data[self.name].address), 1)
        collection = self.book.data[self.name].address
        self.assertIsNotNone(
            self.book.data[self.name].find_item(changed_address, collection)
        )

    def test_contact_phone_number(self):
        phone = "123"
        call_result = add_contact([self.name, phone], self.book)
        self.assertEqual(
            call_result, "Phone number is not correct. Expected format is 10 digits."
        )
        self.assertEqual(len(self.book.data), 0)

        phone = "aaa123bbb3"
        call_result = add_contact([self.name, phone], self.book)
        self.assertEqual(
            call_result, "Phone number is not correct. Expected format is 10 digits."
        )
        self.assertEqual(len(self.book.data), 0)

    def test_contact_email(self):
        pass

    # email = "abc@1"
    # call_result = add_contact([self.name, self.phone], self.book)


if __name__ == "__main__":
    unittest.main()
