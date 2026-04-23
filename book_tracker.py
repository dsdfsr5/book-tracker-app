import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class BookTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker - Прочитанные книги")
        self.root.geometry("750x500")
        
        # Данные: список книг
        self.books = []
        self.filtered_books = []
        
        # --- Поля ввода ---
        input_frame = tk.LabelFrame(root, text="Добавление книги", padx=10, pady=10)
        input_frame.pack(padx=10, pady=10, fill="x")
        
        tk.Label(input_frame, text="Название:").grid(row=0, column=0, sticky="w")
        self.title_entry = tk.Entry(input_frame, width=30)
        self.title_entry.grid(row=0, column=1, padx=5)
        
        tk.Label(input_frame, text="Автор:").grid(row=0, column=2, sticky="w")
        self.author_entry = tk.Entry(input_frame, width=20)
        self.author_entry.grid(row=0, column=3, padx=5)
        
        tk.Label(input_frame, text="Жанр:").grid(row=1, column=0, sticky="w")
        self.genre_entry = tk.Entry(input_frame, width=20)
        self.genre_entry.grid(row=1, column=1, padx=5)
        
        tk.Label(input_frame, text="Страниц:").grid(row=1, column=2, sticky="w")
        self.pages_entry = tk.Entry(input_frame, width=10)
        self.pages_entry.grid(row=1, column=3, padx=5, sticky="w")
        
        add_btn = tk.Button(input_frame, text="Добавить книгу", command=self.add_book, bg="lightgreen")
        add_btn.grid(row=2, column=0, columnspan=4, pady=10)
        
        # --- Фильтры ---
        filter_frame = tk.LabelFrame(root, text="Фильтрация", padx=10, pady=10)
        filter_frame.pack(padx=10, pady=5, fill="x")
        
        tk.Label(filter_frame, text="Фильтр по жанру:").pack(side="left")
        self.filter_genre_entry = tk.Entry(filter_frame, width=15)
        self.filter_genre_entry.pack(side="left", padx=5)
        
        tk.Label(filter_frame, text="Страниц >").pack(side="left", padx=(10,0))
        self.filter_pages_entry = tk.Entry(filter_frame, width=5)
        self.filter_pages_entry.pack(side="left", padx=5)
        
        filter_btn = tk.Button(filter_frame, text="Применить фильтр", command=self.apply_filter)
        filter_btn.pack(side="left", padx=10)
        
        reset_btn = tk.Button(filter_frame, text="Сбросить фильтр", command=self.reset_filter)
        reset_btn.pack(side="left")
        
        # --- Таблица книг ---
        columns = ("Название", "Автор", "Жанр", "Страницы")
        self.tree = ttk.Treeview(root, columns=columns, show="headings", height=15)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        self.tree.pack(padx=10, pady=10, fill="both", expand=True)
        
        # --- Кнопки сохранения/загрузки ---
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)
        
        save_btn = tk.Button(btn_frame, text="Сохранить в JSON", command=self.save_to_json, bg="lightblue")
        save_btn.pack(side="left", padx=5)
        
        load_btn = tk.Button(btn_frame, text="Загрузить из JSON", command=self.load_from_json, bg="lightyellow")
        load_btn.pack(side="left", padx=5)
        
        # Загружаем данные при старте (если есть)
        self.load_from_json()
    
    def add_book(self):
        # Валидация
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        genre = self.genre_entry.get().strip()
        pages_str = self.pages_entry.get().strip()
        
        if not title or not author or not genre:
            messagebox.showerror("Ошибка", "Все поля (Название, Автор, Жанр) должны быть заполнены!")
            return
        
        if not pages_str:
            messagebox.showerror("Ошибка", "Введите количество страниц!")
            return
        
        if not pages_str.isdigit():
            messagebox.showerror("Ошибка", "Количество страниц должно быть числом!")
            return
        
        pages = int(pages_str)
        
        book = {
            "title": title,
            "author": author,
            "genre": genre,
            "pages": pages
        }
        self.books.append(book)
        self.reset_filter()  # Обновляем отображение
        self.clear_entries()
        messagebox.showinfo("Успех", f"Книга '{title}' добавлена!")
    
    def clear_entries(self):
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.pages_entry.delete(0, tk.END)
    
    def apply_filter(self):
        genre_filter = self.filter_genre_entry.get().strip().lower()
        pages_filter_str = self.filter_pages_entry.get().strip()
        
        self.filtered_books = self.books.copy()
        
        if genre_filter:
            self.filtered_books = [b for b in self.filtered_books if genre_filter in b["genre"].lower()]
        
        if pages_filter_str:
            if pages_filter_str.isdigit():
                pages_threshold = int(pages_filter_str)
                self.filtered_books = [b for b in self.filtered_books if b["pages"] > pages_threshold]
            else:
                messagebox.showerror("Ошибка фильтра", "Фильтр по страницам должен быть числом!")
                return
        
        self.update_table(self.filtered_books)
    
    def reset_filter(self):
        self.filter_genre_entry.delete(0, tk.END)
        self.filter_pages_entry.delete(0, tk.END)
        self.update_table(self.books)
    
    def update_table(self, books_list):
        # Очищаем таблицу
        for row in self.tree.get_children():
            self.tree.delete(row)
        # Заполняем
        for book in books_list:
            self.tree.insert("", tk.END, values=(book["title"], book["author"], book["genre"], book["pages"]))
    
    def save_to_json(self):
        try:
            with open("books.json", "w", encoding="utf-8") as f:
                json.dump(self.books, f, ensure_ascii=False, indent=4)
            messagebox.showinfo("Сохранено", "Данные сохранены в books.json")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить: {e}")
    
    def load_from_json(self):
        if not os.path.exists("books.json"):
            return  # Нет файла - ничего не загружаем
        try:
            with open("books.json", "r", encoding="utf-8") as f:
                self.books = json.load(f)
            self.reset_filter()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BookTracker(root)
    root.mainloop()