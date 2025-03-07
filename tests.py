from main import BooksCollector
import pytest

# класс TestBooksCollector объединят набор тестов, которыми мы покрываем наше приложение BooksCollector
# обязательно указывать пофекс Test
class TestBooksCollector:

    # пример теста:
    # обязательно указывать префикс test_
    # дальше идет название метода, который тестируем add_new_book_
    # затем, что тестируем add_two_books - добавление двух книг
    def test_add_new_book_add_two_books(self):
        # создаем экземпляр (объект) класса BooksCollector
        collector = BooksCollector()

        collector.add_new_book("Гордость и предубеждение и зомби")
        collector.add_new_book("Что делать, если ваш кот хочет вас убить")

        # словарь books_rating, который нам возвращает метод get_books_rating, имеет длину 2
        assert len(collector.get_books_rating()) == 2

class TestBooksCollectorNew:
    @pytest.fixture()
    def collector(self):
        return BooksCollector()

    @pytest.mark.parametrize(
        "book_name, expected",
        [("Война миров", True), ("Слияние", True), ("", False), ("A" * 41, False)],
    )
    def test_add_new_book(self, collector, book_name, expected):
        collector.add_new_book(book_name)
        assert(book_name in collector.get_books_genre()) == expected

    @pytest.mark.parametrize(
        "book_name, genre, expected_genre",
        [
        ("Война миров", "Фантастика", "Фантастика"),
        ("Сияние", "Ужасы", "Ужасы"),
        ("Война миров", "Неизвестный жанр", ""),
        ("Такой книги нет", "Фонтастика", None),
        ],
    )
    def test_set_book_genre(self, collector, book_name, genre, expected_genre):
        collector.add_new_book("Война миров")
        collector.add_new_book("Сияние")
        collector.set_book_genre(book_name, genre)
        assert collector.get_book_genre(book_name) == expected_genre
