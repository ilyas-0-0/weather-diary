import json
import os
import tkinter as tk
from datetime import datetime
from tkinter import ttk, messagebox


class WeatherDiaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Diary")
        self.data_file = "weather_data.json"
        self.records = self.load_data()

        # Поля ввода
        frame_input = ttk.LabelFrame(root, text="Новая запись")
        frame_input.pack(padx=10, pady=5, fill="x")

        ttk.Label(frame_input, text="Дата (ДД.ММ.ГГГГ):").grid(row=0, column=0, padx=5, pady=5)
        self.entry_date = ttk.Entry(frame_input)
        self.entry_date.insert(0, datetime.now().strftime("%d.%m.%Y"))
        self.entry_date.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_input, text="Температура (°C):").grid(row=1, column=0, padx=5, pady=5)
        self.entry_temp = ttk.Entry(frame_input)
        self.entry_temp.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame_input, text="Описание:").grid(row=2, column=0, padx=5, pady=5)
        self.entry_desc = ttk.Entry(frame_input)
        self.entry_desc.grid(row=2, column=1, padx=5, pady=5)

        self.precip_var = tk.BooleanVar()
        ttk.Checkbutton(frame_input, text="Осадки", variable=self.precip_var).grid(row=3, columnspan=2)

        ttk.Button(frame_input, text="Добавить запись", command=self.add_record).grid(row=4, columnspan=2, pady=10)

        # Фильтрация
        frame_filter = ttk.LabelFrame(root, text="Фильтрация")
        frame_filter.pack(padx=10, pady=5, fill="x")

        ttk.Label(frame_filter, text="Мин. темп:").grid(row=0, column=0, padx=5, pady=5)
        self.filter_temp = ttk.Entry(frame_filter, width=10)
        self.filter_temp.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(frame_filter, text="Применить фильтр", command=self.update_table).grid(row=0, column=2, padx=5)
        ttk.Button(frame_filter, text="Сброс", command=self.reset_filter).grid(row=0, column=3, padx=5)

        # Таблица
        self.tree = ttk.Treeview(root, columns=("date", "temp", "desc", "precip"), show="headings")
        self.tree.heading("date", text="Дата")
        self.tree.heading("temp", text="Темп. °C")
        self.tree.heading("desc", text="Описание")
        self.tree.heading("precip", text="Осадки")
        self.tree.pack(padx=10, pady=10, fill="both", expand=True)

        self.update_table()

    def validate(self):
        try:
            datetime.strptime(self.entry_date.get(), "%d.%m.%Y")
            float(self.entry_temp.get())
            if not self.entry_desc.get().strip():
                raise ValueError("Описание пустое")
            return True
        except ValueError as e:
            messagebox.showerror("Ошибка", f"Некорректные данные: {e}")
            return False

    def add_record(self):
        if self.validate():
            record = {
                "date": self.entry_date.get(),
                "temp": float(self.entry_temp.get()),
                "desc": self.entry_desc.get().strip(),
                "precip": "Да" if self.precip_var.get() else "Нет"
            }
            self.records.append(record)
            self.save_data()
            self.update_table()
            self.entry_temp.delete(0, tk.END)
            self.entry_desc.delete(0, tk.END)

    def update_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        f_temp = self.filter_temp.get()

        for r in self.records:
            if f_temp and r['temp'] < float(f_temp):
                continue
            self.tree.insert("", "end", values=(r['date'], r['temp'], r['desc'], r['precip']))

    def reset_filter(self):
        self.filter_temp.delete(0, tk.END)
        self.update_table()

    def save_data(self):
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.records, f, ensure_ascii=False, indent=4)

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []


if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherDiaryApp(root)
    root.mainloop()
