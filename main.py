import tkinter as tk
from tkinter import filedialog, colorchooser
from tkinter import ttk
from PIL import Image, ImageTk
import numpy as np
import colorsys
import os


class ColorChangerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cambio de Color en Imagen")

        # Variables
        self.image_path = None
        self.original_image = None
        self.modified_image = None

        # Frame de botones
        frame_botones = tk.Frame(root)
        frame_botones.pack(pady=10)

        # Botón para cargar la imagen
        btn_cargar = ttk.Button(frame_botones, text="Cargar Imagen", command=self.cargar_imagen)
        btn_cargar.grid(row=0, column=0, padx=10)

        # Botón para seleccionar color
        btn_color = ttk.Button(frame_botones, text="Seleccionar Color", command=self.seleccionar_color)
        btn_color.grid(row=0, column=1, padx=10)

        # Botón para descargar imagen
        btn_descargar = ttk.Button(frame_botones, text="Descargar Imagen", command=self.descargar_imagen)
        btn_descargar.grid(row=0, column=2, padx=10)

        # Label para la vista previa de la imagen
        self.label_imagen = tk.Label(root)
        self.label_imagen.pack(pady=10)

    def cargar_imagen(self):
        """Función para cargar la imagen desde el sistema de archivos."""
        self.image_path = filedialog.askopenfilename(filetypes=[("Imagenes", "*.png;*.jpg;*.jpeg")])
        if self.image_path:
            self.original_image = Image.open(self.image_path)
            self.mostrar_imagen(self.original_image)

    def seleccionar_color(self):
        """Función para seleccionar un color y cambiar los tonos de la imagen."""
        if self.original_image is None:
            return

        # Selección del color mediante el selector de color
        color_seleccionado = colorchooser.askcolor()[0]
        if color_seleccionado:
            nuevo_tono = self.rgb_a_hue(color_seleccionado)
            self.modified_image = self.cambiar_tono(self.original_image, nuevo_tono)
            self.mostrar_imagen(self.modified_image)

    def cambiar_tono(self, imagen, nuevo_tono):
        """Función para cambiar el tono de la imagen manteniendo la saturación y el brillo."""
        img_np = np.array(imagen.convert('RGB')) / 255.0  # Normalizar a rango [0, 1]
        nueva_img_np = np.zeros_like(img_np)

        # Convertir cada píxel de RGB a HSV, modificar el tono (hue), y regresar a RGB
        for i in range(img_np.shape[0]):
            for j in range(img_np.shape[1]):
                r, g, b = img_np[i, j]
                h, s, v = colorsys.rgb_to_hsv(r, g, b)
                nuevo_rgb = colorsys.hsv_to_rgb(nuevo_tono, s, v)  # Mantener saturación y valor
                nueva_img_np[i, j] = nuevo_rgb

        # Convertir el array de vuelta a una imagen (denormalizando a rango [0, 255])
        nueva_img = Image.fromarray((nueva_img_np * 255).astype(np.uint8))
        return nueva_img

    def mostrar_imagen(self, imagen):
        """Función para mostrar la imagen en la interfaz con un escalado si es pequeña."""
        # Tamaño mínimo de vista previa
        ancho_minimo, alto_minimo = 400, 400

        # Obtener dimensiones originales
        ancho_original, alto_original = imagen.size

        # Si la imagen tiene canal alfa (transparencia)
        if imagen.mode == 'RGBA':
            # Crear un fondo blanco temporal
            imagen_fondo = Image.new("RGBA", imagen.size, (255, 255, 255, 0))
            imagen_fondo.paste(imagen, (0, 0), imagen)
            imagen = imagen_fondo

        # Si la imagen es pequeña, escalar con "nearest" (sin suavizado)
        if ancho_original < ancho_minimo or alto_original < alto_minimo:
            factor_escala = max(ancho_minimo // ancho_original, alto_minimo // alto_original)
            imagen_preview = imagen.resize((ancho_original * factor_escala, alto_original * factor_escala),
                                           Image.Resampling.NEAREST)
        else:
            # Si la imagen es suficientemente grande, usar escalado con suavizado
            imagen_preview = imagen.resize((ancho_minimo, alto_minimo), Image.Resampling.LANCZOS)

        img_tk = ImageTk.PhotoImage(imagen_preview)
        self.label_imagen.config(image=img_tk)
        self.label_imagen.image = img_tk  # Guardar referencia para evitar el garbage collection

    def descargar_imagen(self):
        """Función para guardar la imagen modificada."""
        if self.modified_image:
            ruta_guardar = filedialog.asksaveasfilename(defaultextension=".png",
                                                        filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
            if ruta_guardar:
                self.modified_image.save(ruta_guardar)
                print(f"Imagen guardada en: {ruta_guardar}")

    def rgb_a_hue(self, rgb):
        """Convierte un color RGB a su valor de Hue (tono) en el espacio HSV."""
        r, g, b = [x / 255.0 for x in rgb]
        h, _, _ = colorsys.rgb_to_hsv(r, g, b)
        return h


# Inicializar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = ColorChangerApp(root)
    root.mainloop()
