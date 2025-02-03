import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class PoteauCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calcul du Poteau en Béton Armé")
        self.root.geometry("800x800")

        # Style moderne
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#f4f4f4")
        self.style.configure("TLabel", background="#f4f4f4", font=("Arial", 12))
        self.style.configure(
            "TButton",
            background="#007BFF",
            foreground="white",
            font=("Arial", 12, "bold"),
        )
        self.style.configure("TCombobox", font=("Arial", 12))

        # Création des onglets
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        # Onglets
        self.create_dimension_tab()
        self.create_material_tab()
        self.create_norme_tab()
        self.create_sollicitation_tab()
        self.create_result_tab()

        # Bouton de calcul stylisé
        self.calculate_button = ttk.Button(
            root, text="Calculer", command=self.calculate
        )
        self.calculate_button.pack(pady=20)

    def create_dimension_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Dimensions")

        ttk.Label(tab, text="Type de section :").grid(row=0, column=0, padx=10, pady=5)
        self.section_combobox = ttk.Combobox(
            tab, values=["Rectangulaire", "Circulaire"], font=("Arial", 12)
        )
        self.section_combobox.grid(row=0, column=1)
        self.section_combobox.current(0)
        self.section_combobox.bind("<<ComboboxSelected>>", self.update_dimension_fields)

        self.dimension_frame = ttk.Frame(tab)
        self.dimension_frame.grid(row=1, column=0, columnspan=2, pady=10)
        self.update_dimension_fields()

        # Zone pour afficher le schéma
        self.fig, self.ax = plt.subplots(figsize=(3, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=tab)
        self.canvas.get_tk_widget().grid(row=2, column=0, columnspan=2, pady=10)
        self.update_schema()

    def update_dimension_fields(self, event=None):
        for widget in self.dimension_frame.winfo_children():
            widget.destroy()

        section_type = self.section_combobox.get()
        if section_type == "Rectangulaire":
            ttk.Label(self.dimension_frame, text="Largeur (m) :").grid(
                row=0, column=0, padx=10, pady=5
            )
            self.largeur_entry = ttk.Entry(self.dimension_frame, font=("Arial", 12))
            self.largeur_entry.grid(row=0, column=1)

            ttk.Label(self.dimension_frame, text="Hauteur (m) :").grid(
                row=1, column=0, padx=10, pady=5
            )
            self.hauteur_entry = ttk.Entry(self.dimension_frame, font=("Arial", 12))
            self.hauteur_entry.grid(row=1, column=1)
        else:
            ttk.Label(self.dimension_frame, text="Diamètre (m) :").grid(
                row=0, column=0, padx=10, pady=5
            )
            self.diametre_entry = ttk.Entry(self.dimension_frame, font=("Arial", 12))
            self.diametre_entry.grid(row=0, column=1)

        ttk.Label(self.dimension_frame, text="Longueur (m) :").grid(
            row=2, column=0, padx=10, pady=5
        )
        self.longueur_entry = ttk.Entry(self.dimension_frame, font=("Arial", 12))
        self.longueur_entry.grid(row=2, column=1)

    def create_material_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Matériaux")

        ttk.Label(tab, text="Fc28 (MPa) :").grid(row=0, column=0, padx=10, pady=5)
        self.fc28_entry = ttk.Entry(tab, font=("Arial", 12))
        self.fc28_entry.grid(row=0, column=1)

        ttk.Label(tab, text="Densité Béton (kg/m³) :").grid(
            row=1, column=0, padx=10, pady=5
        )
        self.densite_beton_entry = ttk.Entry(tab, font=("Arial", 12))
        self.densite_beton_entry.grid(row=1, column=1)

        ttk.Label(tab, text="Fe Longitudinal (MPa) :").grid(
            row=2, column=0, padx=10, pady=5
        )
        self.fe_long_entry = ttk.Entry(tab, font=("Arial", 12))
        self.fe_long_entry.grid(row=2, column=1)

        ttk.Label(tab, text="Fe Transversal (MPa) :").grid(
            row=3, column=0, padx=10, pady=5
        )
        self.fe_trans_entry = ttk.Entry(tab, font=("Arial", 12))
        self.fe_trans_entry.grid(row=3, column=1)

    def create_norme_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Normes")

        ttk.Label(tab, text="Norme de Calcul :").grid(row=0, column=0, padx=10, pady=5)
        self.norme_combobox = ttk.Combobox(
            tab, values=["BAEL 91", "Eurocode 2"], font=("Arial", 12)
        )
        self.norme_combobox.grid(row=0, column=1)
        self.norme_combobox.current(0)

    def calculate(self):
        result_text = "Norme utilisée: {}\n".format(self.norme_combobox.get())
        result_text += "État: ELU & ELS\n"
        result_text += "Section acier longitudinal: À calculer\n"
        result_text += "Section acier transversal: À calculer\n"

        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, result_text)


if __name__ == "__main__":
    root = tk.Tk()
    app = PoteauCalculatorApp(root)
    root.mainloop()
