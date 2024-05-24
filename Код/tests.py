#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Для индивидуального задания лабораторной работы 2.21 добавьте тесты с использованием
модуля unittest, проверяющие операции по работе с базой данных.
"""
import unittest
import sqlite3
from io import StringIO
import sys

# Функции для работы с базой данных
def display_table(headers, data):
    """
    Отображает данные в виде таблицы.
    """
    print("┌", end="")
    for header in headers[:-1]:
        print("─" * 20 + "┬", end="")
    print("─" * 20 + "┐")
    
    print("│", end="")
    for header in headers:
        print(f" {header:<18}│", end="")
    print("\n├", end="")
    for header in headers[:-1]:
        print("─" * 20 + "┼", end="")
    print("─" * 20 + "┤")
    
    for row in data:
        print("│", end="")
        for item in row:
            print(f" {item:<18}│", end="")
        print()
        
    print("└", end="")
    for header in headers[:-1]:
        print("─" * 20 + "┴", end="")
    print("─" * 20 + "┘")


def find_store(cursor, store_id):
    """
    Находит магазин по его идентификатору.
    """
    cursor.execute('SELECT * FROM stores WHERE store_id = ?', (store_id,))
    store = cursor.fetchone()
    if store:
        print("Найден магазин:")
        print("ID:", store[0])
        print("Название:", store[1])
        print("Адрес:", store[2])
    else:
        print("Магазин с указанным ID не найден.")


# Класс для тестирования
class TestDatabaseOperations(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        # Создание временной базы данных для тестов
        self.conn = sqlite3.connect(':memory:')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE stores (
                                store_id INTEGER PRIMARY KEY,
                                name TEXT NOT NULL,
                                address TEXT NOT NULL)''')
        self.cursor.execute('''CREATE TABLE products (
                                product_id INTEGER PRIMARY KEY,
                                name TEXT NOT NULL,
                                price REAL NOT NULL,
                                store_id INTEGER,
                                FOREIGN KEY(store_id) REFERENCES stores(store_id))''')
        self.cursor.execute("INSERT INTO stores (store_id, name, address) VALUES (1, 'Store A', 'Address A')")
        self.cursor.execute("INSERT INTO stores (store_id, name, address) VALUES (2, 'Store B', 'Address B')")
        self.conn.commit()
    
    def tearDown(self):
        # Закрытие соединения с базой данных
        self.cursor.close()
        self.conn.close()
    
    def test_display_table(self):
        # Перенаправление вывода для теста
        captured_output = StringIO()
        sys.stdout = captured_output
        
        # Тестирование отображения таблицы магазинов
        self.cursor.execute('SELECT * FROM stores')
        stores = self.cursor.fetchall()
        display_table(['ID', 'Название', 'Адрес'], stores)
        
        # Проверка результата
        expected_output = (
            "┌────────────────────┬────────────────────┬────────────────────┐\n"
            "│ ID                 │ Название           │ Адрес              │\n"
            "├────────────────────┼────────────────────┼────────────────────┤\n"
            "│ 1                  │ Store A            │ Address A          │\n"
            "│ 2                  │ Store B            │ Address B          │\n"
            "└────────────────────┴────────────────────┴────────────────────┘\n"
        )
        self.assertEqual(captured_output.getvalue(), expected_output)
        
        # Восстановление стандартного вывода
        sys.stdout = sys.__stdout__
    
    def test_find_store(self):
        # Перенаправление вывода для теста
        captured_output = StringIO()
        sys.stdout = captured_output
        
        # Тестирование поиска магазина по идентификатору
        find_store(self.cursor, 1)
        
        # Проверка результата
        expected_output = "Найден магазин:\nID: 1\nНазвание: Store A\nАдрес: Address A\n"
        self.assertIn(expected_output, captured_output.getvalue())
        
        # Очистка вывода
        captured_output.truncate(0)
        captured_output.seek(0)
        
        # Тестирование поиска несуществующего магазина
        find_store(self.cursor, 3)
        
        # Проверка результата
        expected_output = "Магазин с указанным ID не найден.\n"
        self.assertIn(expected_output, captured_output.getvalue())
        
        # Восстановление стандартного вывода
        sys.stdout = sys.__stdout__


# Запуск тестов
if __name__ == '__main__':
    unittest.main()

