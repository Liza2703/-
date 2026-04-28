import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import re

DATA_FILE = "data.json"

# --- Глобальные переменные ---
trainings = []
displayed_trainings = []

# --- Основные функции ---
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {e}")
    return []

def save_data():
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(trainings, f, ensure_ascii=False, indent=4)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось сохранить данные: {e}")

def update_treeview():
    for i in tree.get_children():
        tree.delete(i)
    for tr in displayed_trainings:
        tree.insert("", tk.END, values=(tr["date"], tr["type"], tr["duration"]))

def add_training():
    date = date_entry.get().strip()
    duration_str = duration_entry.get().strip()
    tr_type = type_var.get()

    try:
        if not duration_str:
            raise ValueError("Длительность не может быть пустой.")
        duration = int(duration_str)
        if duration <= 0:
            raise ValueError("Длительность должна быть больше нуля.")
        if not tr_type:
            raise ValueError("Выберите тип тренировки.")
        if not re.match(r"^\d{2}\.\d{2}\.\d{4}$", date):
            raise ValueError("Неверный формат даты. Используйте ДД.ММ.ГГГГ.")

        trainings.append({"date": date, "type": tr_type, "duration": duration})
        displayed_trainings.clear()
        displayed_trainings.extend(trainings)
        update_treeview()

        date_entry.delete(0, tk.END)
        duration_entry.delete(0, tk.END)
        save_data()
        messagebox.showinfo("Успех", "Тренировка добавлена!")
    except ValueError as e:
        messagebox.showerror("Ошибка", str(e))

def apply_filter():
    filter_type = filter_type_var.get()
    filter_date = filter_date_entry.get().strip()

    filtered = [tr for tr in trainings if (filter_type == "Все" or tr["type"] == filter_type) and (not filter_date or tr["date"] == filter_date)]
    displayed_trainings.clear()
    displayed_trainings.extend(filtered)
    update_treeview()

def reset_filter():
    filter_type_var.set("Все")
    filter_date_entry.delete(0, tk.END)
    displayed_trainings.clear()
    displayed_trainings.extend(trainings)
    update_treeview()

# --- Инициализация данных ---
trainings = load_data()
displayed_trainings = trainings.copy()

# --- Создание окна ---
root = tk.Tk()
root.title("Training Planner")
root.geometry("900x600")

# Фильтр
filter_frame = ttk.LabelFrame(root, text="Фильтр", padding="5")
filter_frame.pack(fill="x", padx=10, pady=5)

ttk.Label(filter_frame, text="Тип:").pack(side="left", padx=5)
filter_type_var = tk.StringVar(value="Все")
type_options = ["Все", "Кардио", "Силовая", "Растяжка", "Йога"]
ttk.Combobox(filter_frame, textvariable=filter_type_var, values=type_options, state="readonly", width=12).pack(side="left", padx=5)

ttk.Label(filter_frame, text="Дата (ДД.ММ.ГГГГ):").pack(side="left", padx=5)
filter_date_entry = ttk.Entry(filter_frame, width=12)
filter_date_entry.pack(side="left", padx=5)

ttk.Button(filter_frame, text="Применить фильтр", command=apply_filter).pack(side="left", padx=5)

# Ввод данных
input_frame = ttk.LabelFrame(root, text="Добавить тренировку", padding="10")
input_frame.pack(fill="x", padx=10, pady=5)

ttk.Label(input_frame, text="Дата (ДД.ММ.ГГГГ):").grid(row=0, column=0, sticky="w", pady=2)
date_entry = ttk.Entry(input_frame, width=20)
date_entry.grid(row=0, column=1, sticky="we", pady=2)

ttk.Label(input_frame, text="Тип:").grid(row=1, column=0, sticky="w", pady=2)
type_var = tk.StringVar()
type_values = ["Кардио", "Силовая", "Растяжка", "Йога"]
ttk.Combobox(input_frame, textvariable=type_var, values=type_values, state="readonly", width=17).grid(row=1, column=1, sticky="we", pady=2)
type_var.set(type_values[0])

ttk.Label(input_frame, text="Длительность (мин):").grid(row=2, column=0, sticky="w", pady=2)
duration_entry = ttk.Entry(input_frame, width=20)
duration_entry.grid(row=2, column=1, sticky="we", pady=2)

ttk.Button(input_frame, text="Добавить тренировку", command=add_training).grid(row=3, column=0, columnspan=2, pady=10)

# Кнопки управления фильтром
btn_frame = ttk.Frame(root)
btn_frame.pack(fill="x", padx=10, pady=5)
ttk.Button(btn_frame, text="Сбросить фильтр / Показать все", command=reset_filter).pack(side="left")

# Таблица тренировок
table_container = ttk.Frame(root)
table_container.pack(fill='both', expand=True, padx=10, pady=5)

yscrollbar = ttk.Scrollbar(table_container, orient="vertical")
xscrollbar = ttk.Scrollbar(table_container, orient="horizontal")
tree = ttk.Treeview(table_container,
                    columns=("date", "type", "duration"),
                    show='headings',
                    yscrollcommand=yscrollbar.set,
                    xscrollcommand=xscrollbar.set)
yscrollbar.config(command=tree.yview)
xscrollbar.config(command=tree.xview)
tree.heading("date", text="Дата")
tree.heading("type", text="Тип")
tree.heading("duration", text="Длительность (мин)")
tree.grid(row=0, column=0, sticky='nsew')
yscrollbar.grid(row=0, column=1, sticky='ns')
xscrollbar.grid(row=1, column=0, sticky='ew')
table_container.grid_rowconfigure(0, weight=1)
table_container.grid_columnconfigure(0, weight=1)

update_treeview()
root.mainloop()
