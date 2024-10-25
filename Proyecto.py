import tkinter as tk
from tkinter import Button, Toplevel, ttk, messagebox
from matplotlib import pyplot as plt
import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Clase para la Calculadora de Álgebra Lineal
class MatrixCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora Multifuncional de Matrices")
        self.root.geometry("800x600")
        self.root.configure(bg="#282a36")  # Fondo de atras 

        # Estilos
        self.style = ttk.Style()
        self.style.theme_use('clam')  # tema compatible con cambios de color
        self.style.configure('TButton', font=('Helvetica', 10, 'bold'), padding=10, background='#6272a4')
        self.style.map("TButton", background=[('active', '#44475a')])
        self.style.configure('TButton', font=('Helvetica', 10, 'bold'), padding=10)
        self.style.configure('TLabel', font=('Helvetica', 10))
        self.style.configure('Header.TLabel', font=('Helvetica', 14, 'bold'), foreground="#fdfcfb")
        self.style.configure('TFrame', background='#282a36')

        # Header
        header = ttk.Label(root, text="Calculadora Multifuncional de Matrices", style='Header.TLabel', background="#282a36")
        header.pack(pady=10)

        # Marco para seleccionar tamaño de matriz
        size_frame = ttk.Frame(root, padding=10, borderwidth=2, relief="groove")
        size_frame.pack(pady=10, padx=10, fill='x')

        size_label = ttk.Label(size_frame, text="Tamaño de la matriz (n x n):", style='TLabel')
        size_label.grid(row=0, column=0, padx=5, pady=5, sticky='W')

        self.size_entry = ttk.Entry(size_frame, width=5)
        self.size_entry.grid(row=0, column=1, padx=5, pady=5, sticky='W')

        generate_button = ttk.Button(size_frame, text="Generar Matriz", command=self.generate_matrix)
        generate_button.grid(row=0, column=2, padx=10, pady=5)

        # Marco para ingresar matrices
        self.matrix_frame = ttk.Frame(root, padding=10, borderwidth=2, relief="groove")
        self.matrix_frame.pack(pady=10, padx=10, fill='both')

        # Marco para botones de operaciones
        operations_frame = ttk.Frame(root, padding=10, borderwidth=2, relief="groove")
        operations_frame.pack(pady=10, padx=10, fill='x')