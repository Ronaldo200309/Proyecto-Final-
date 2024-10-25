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

        # Botones para las operaciones 
        gauss_button = ttk.Button(operations_frame, text="Método Gauss-Jordan", command=self.gauss_jordan)
        gauss_button.grid(row=0, column=0, padx=10, pady=5)

        cramer_button = ttk.Button(operations_frame, text="Regla de Cramer", command=self.cramer)
        cramer_button.grid(row=0, column=1, padx=10, pady=5)

        multiply_button = ttk.Button(operations_frame, text="Multiplicación de Matrices", command=self.multiply)
        multiply_button.grid(row=0, column=2, padx=10, pady=5)

        inverse_button = ttk.Button(operations_frame, text="Calcular Inversa", command=self.inverse)
        inverse_button.grid(row=0, column=3, padx=10, pady=5)

        # Botón para graficar ecuaciones
        plot_button = ttk.Button(operations_frame, text="Graficar Ecuaciones", command=self.plot_equations)
        plot_button.grid(row=0, column=4, padx=10, pady=5)

        # Marco para resultados
        result_frame = ttk.Frame(root, padding=10, borderwidth=2, relief="groove")
        result_frame.pack(pady=10, padx=10, fill='both', expand=True)

        result_label = ttk.Label(result_frame, text="Resultados:", style='Header.TLabel', background="#282a36")
        result_label.pack(anchor='w')

        self.result_text = tk.Text(result_frame, height=10, wrap='word', bg="#44475a", fg="White", font=('Helvetica', 17), borderwidth=2)
        self.result_text.pack(fill='both', expand=True)

        # Variables que sirven para almacenar las entradas de las matrices 
        self.matrix_entries = []
        self.second_matrix_entries = []
        self.cramer_entries = []  # Entrada para el método de Cramer

    # Método para generar matrices según el tamaño que se especifique
    def generate_matrix(self):
        # limpia el marco de las matrices anteriores 
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()
        self.matrix_entries = []
        self.second_matrix_entries = []
        self.cramer_entries = []

        try:
            size = int(self.size_entry.get())
            if size < 2 or size > 5:
                messagebox.showerror("Error", "Por favor, ingrese un tamaño entre 2 y 5.")
                return
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese un número válido para el tamaño de la matriz.")
            return

        # Crea pestañas para las diferentes matrices 
        self.notebook = ttk.Notebook(self.matrix_frame)
        self.notebook.pack(fill='both', expand=True)
        
        # Matriz A
        self.tab1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text='Matriz A')

        ttk.Label(self.tab1, text="Ingrese los elementos de la Matriz A:", background='#282a36', foreground='white').pack(pady=5)

        matrix_a_frame = ttk.Frame(self.tab1)
        matrix_a_frame.pack()

        for i in range(size):
            row = []
            for j in range(size):
                entry = ttk.Entry(matrix_a_frame, width=5, justify='center')
                entry.grid(row=i, column=j, padx=2, pady=2)
                row.append(entry)
            self.matrix_entries.append(row)

        # Matriz B
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab2, text='Matriz B')

        ttk.Label(self.tab2, text="Ingrese los elementos de la Matriz B:", background='#282a36', foreground='white').pack(pady=5)

        matrix_b_frame = ttk.Frame(self.tab2)
        matrix_b_frame.pack()

        for i in range(size):
            row = []
            for j in range(size):
                entry = ttk.Entry(matrix_b_frame, width=5, justify='center')
                entry.grid(row=i, column=j, padx=2, pady=2)
                row.append(entry)
            self.second_matrix_entries.append(row)

        # pestaña Matriz para Cramer (n x (n+1))
        self.tab3 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab3, text='Matriz Cramer')

        ttk.Label(self.tab3, text="Ingrese los coeficientes y términos independientes:", background='#282a36', foreground='white').pack(pady=5)

        matrix_cramer_frame = ttk.Frame(self.tab3)
        matrix_cramer_frame.pack()

        for i in range(size):
            row = []
            for j in range(size + 1):  # Matriz extendida (n x (n+1))
                entry = ttk.Entry(matrix_cramer_frame, width=5, justify='center')
                entry.grid(row=i, column=j, padx=2, pady=2)
                row.append(entry)
            self.cramer_entries.append(row)

    def get_matrix(self, entries):
        matrix = []
        try:
            for row in entries:
                matrix_row = []
                for entry in row:
                    value = float(entry.get())
                    matrix_row.append(value)
                matrix.append(matrix_row)
            return np.array(matrix)
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese solo números en las matrices.")
            return None
        
        # Nueva función para graficar ecuaciones en 3D
    def plot_equations(self):
        matrix = self.get_matrix(self.cramer_entries) # Usar la matriz para Cramer
        if matrix is None:
            return

        try:
            # Extraer los coeficientes y términos independientes
            n = matrix.shape[0]
            A = matrix[:, :-1]  # Coeficientes
            b = matrix[:, -1]  # Términos independientes

            # Comprobar si se trata de un sistema 3x3
            if n != 3 or A.shape[1] != 3:
                messagebox.showerror("Error", "Solo se pueden graficar sistemas 3x3 en 3D.")
                return

            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')

            # Generar los puntos para X y Y
            x = np.linspace(-10, 10, 400)
            y = np.linspace(-10, 10, 400)
            X, Y = np.meshgrid(x, y)

            # Calcular Z para cada ecuación
            for i in range(n):
                Z = (b[i] - A[i][0] * X - A[i][1] * Y) / A[i][2]
                ax.plot_surface(X, Y, Z, alpha=0.5, label=f"Ecuación {i+1}")

            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            plt.title("Gráfica de las Ecuaciones en 3D")
            plt.show()
        except Exception as e:
            messagebox.showerror("Error", str(e))

            # Método de Gauss-Jordan mejorado para mostrar el procedimiento completo
    def gauss_jordan(self):
        self.result_text.delete(1.0, tk.END)
        matrix = self.get_matrix(self.matrix_entries)
        if matrix is None:
            return
        try:
            n = matrix.shape[0]
            augmented = np.hstack((matrix, np.eye(n)))  # Matriz aumentada (A | I)
            steps = []

            for i in range(n):
                if np.isclose(augmented[i][i], 0):
                # Intercambiar con una fila que tenga un valor distinto de cero en la columna i
                    for j in range(i + 1, n):
                        if not np.isclose(augmented[j][i], 0):
                            augmented[[i, j]] = augmented[[j, i]]
                            steps.append(f"Intercambio de fila {i + 1} con fila {j + 1}")
                            break
                    else:
                        self.result_text.insert(tk.END, "El sistema no tiene solución o tiene infinitas soluciones.\n")
                        return

                pivot = augmented[i][i]
                augmented[i] = augmented[i] / pivot
                steps.append(f"Dividir fila {i + 1} por {pivot:.3f} para hacer el pivote igual a 1")

                for j in range(n):
                    if j != i:
                        factor = augmented[j][i]
                        augmented[j] -= factor * augmented[i]
                        steps.append(f"Restar {factor:.3f} * fila {i + 1} de fila {j + 1}")

        # Verificar si la matriz tiene una única solución
            if np.all(np.isclose(augmented[:, :-n], np.eye(n))):  # Si la matriz es la identidad
                self.result_text.insert(tk.END, "El sistema tiene solución única:\n")
                solutions = augmented[:, -n:]
                for i, sol in enumerate(solutions):
                    self.result_text.insert(tk.END, f"x{i + 1} = {sol[0]:.3f}\n")
            else:
                 self.result_text.insert(tk.END, "El sistema no tiene solución o tiene infinitas soluciones.\n")

            self.result_text.insert(tk.END, "\nMatriz final después de Gauss-Jordan:\n")
            self.result_text.insert(tk.END, np.round(augmented, 3))  # Imprimir la matriz final

        except Exception as e:
            messagebox.showerror("Error", str(e))

             # Método de Cramer
    def cramer(self):
        self.result_text.delete(1.0, tk.END)
        matrix = self.get_matrix(self.cramer_entries)  # Usar la nueva matriz para Cramer
        if matrix is None:
            return
        try:
            n = matrix.shape[0]
            m = matrix.shape[1]

            if m != n + 1:  # Verifica que la matriz sea (n x (n + 1))
                raise ValueError("La matriz debe ser de tamaño n x (n + 1).")

            A = matrix[:, :-1]  # Coeficientes
            b = matrix[:, -1]  # Términos independientes

            det_A = np.linalg.det(A)
            if det_A == 0:
                raise ValueError("La matriz de coeficientes no es invertible.")

            steps = []
            solutions = []
            for i in range(n):
                # Crear matriz Ai
                Ai = np.copy(A)
                Ai[:, i] = b
                det_Ai = np.linalg.det(Ai)
                x_i = det_Ai / det_A
                solutions.append(x_i)
                steps.append(f"Det(A{i + 1}) = {det_Ai:.3f}, x{i + 1} = {det_Ai:.3f} / {det_A:.3f} = {x_i:.3f}")

            self.result_text.insert(tk.END, "Proceso de la Regla de Cramer:\n")
            for step in steps:
                self.result_text.insert(tk.END, step + "\n")
            self.result_text.insert(tk.END, "\nSoluciones:\n")
            for i, sol in enumerate(solutions):
                self.result_text.insert(tk.END, f"x{i + 1} = {sol:.3f}\n")
        except Exception as e:
            messagebox.showerror("Error", str(e))