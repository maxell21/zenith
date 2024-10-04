import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageEnhance, ImageOps

class Process_image:
    def add_shape(self, image):
        enhancer = ImageEnhance.Sharpness(image)
        return enhancer.enhance(2.0)

    def image_gray(self, image):
        return ImageOps.grayscale(image)
    
    def image_rotate(self, image):
        return image.rotate(-90, expand=True)


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Зенит")
        self.root.geometry("700x500")
        self.image_processor = Process_image()
        self.processed_image = None
        
        # Загрузка изображения логотипа
        self.logo_image = tk.PhotoImage(file="tmp/logo.png")
        self.logo_image = self.logo_image.subsample(2)

        # Верхняя часть окна с логотипом
        self.logo_label = tk.Label(root, image=self.logo_image)
        self.logo_label.pack(pady=20)

        # Кнопка "Загрузить файл"
        self.load_button = tk.Button(root, text="Загрузить файл", command=self.load_file)
        self.load_button.pack(pady=10)

    def error_popup(self):
        popup = tk.Toplevel(root)
        popup.title("Ошибка")
        popup.geometry("300x100")
        popup_label = tk.Label(popup, text="Произошла ошибка!\n Программа будет закрыта")
        popup_label.pack(pady=10)
        close_button = tk.Button(popup, text="Закрыть", command=self.close_2)
        close_button.pack()

    def close_program(self):
        root.destroy()

    def load_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            image = Image.open(file_path)
            self.processed_image = image
            # Удаляем кнопку "Загрузить файл"
            self.load_button.destroy()
            App.image_screen(self, image)
        else:
            App.error_popup(self)
    
    def apply_processing(self, method_name):
        processing_method = getattr(self.image_processor, method_name)
        self.processed_image = processing_method(self.processed_image)
    
    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("jpg files", "*.jpg"), ("All files", "*.*")])
        if file_path:
            self.processed_image.save(file_path)
            self.close_program()
        else:
            App.error_popup(self)
    
    def image_screen(self, image):
        # кнопка резкости
        self.shape_button = tk.Button(self.root, text="Добавить резкость", command=self.apply_processing('add_shape'))
        self.shape_button.pack()
        
        # кнопка ЧБ
        self.gray_button = tk.Button(self.root, text="Преобразовать в ЧБ", command= lambda: self.apply_processing('image_gray'))
        self.gray_button.pack()
        
        # кнопка поворота
        self.rotate_button = tk.Button(self.root, text="Повернуть на 90 градусов", command=lambda: self.apply_processing('image_rotate'))
        self.rotate_button.pack()
        
        # кнопка сохранения
        self.save_button = tk.Button(self.root, text="Сохранить", command=lambda: self.save_image())
        self.save_button.pack()

            
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()