import tkinter as tk
from tkinter import ttk


class PoteauCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculateur de Poteaux en Béton Armé")

        # Configuration du style
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Création des onglets
        self.notebook = ttk.Notebook(root)

        # Onglet Dimensions
        self.tab_dimensions = ttk.Frame(self.notebook)
        self.create_dimensions_tab()

        # Onglet Matériaux
        self.tab_materials = ttk.Frame(self.notebook)
        self.create_materials_tab()

        # Onglet Normes
        self.tab_standards = ttk.Frame(self.notebook)
        self.create_standards_tab()

        # Onglet Sollicitations
        self.tab_solicitations = ttk.Frame(self.notebook)
        self.create_solicitations_tab()

        self.notebook.add(self.tab_dimensions, text='📏 Dimensions')
        self.notebook.add(self.tab_materials, text='🧱 Matériaux')
        self.notebook.add(self.tab_standards, text='📜 Normes')
        self.notebook.add(self.tab_solicitations, text='⚡ Type de sollicitation')

        self.notebook.pack(expand=1, fill='both', padx=10, pady=10)

        # Bouton de calcul
        btn_calculate = ttk.Button(root, text="Lancer le calcul", command=self.run_calculation)
        btn_calculate.pack(pady=10)

    def create_dimensions_tab(self):
        # Section forme du poteau
        shape_frame = ttk.LabelFrame(self.tab_dimensions, text="Forme du poteau")
        shape_frame.pack(padx=10, pady=5, fill='x')

        self.shape_var = tk.StringVar(value='rectangulaire')
        ttk.Radiobutton(shape_frame,
                        text="Rectangulaire",
                        variable=self.shape_var,
                        value='rectangulaire',
                        command=self.update_dimension_fields).pack(side='left', padx=5)
        ttk.Radiobutton(shape_frame,
                        text="Circulaire",
                        variable=self.shape_var,
                        value='circulaire',
                        command=self.update_dimension_fields).pack(side='left', padx=5)

        # Champs dynamiques selon la forme
        self.dim_fields_frame = ttk.Frame(self.tab_dimensions)
        self.dim_fields_frame.pack(padx=10, pady=5, fill='x')

        # Hauteur commune (en cm)
        ttk.Label(self.dim_fields_frame, text="Hauteur du poteau (cm):").grid(row=0, column=0, sticky='w')
        self.hauteur_entry = ttk.Entry(self.dim_fields_frame)
        self.hauteur_entry.grid(row=0, column=1, padx=5, pady=2)

        # Champs initiaux
        self.update_dimension_fields()

    def update_dimension_fields(self):
        # Nettoyer les anciens champs
        for widget in self.dim_fields_frame.winfo_children()[2:]:
            widget.destroy()

        if self.shape_var.get() == 'rectangulaire':
            ttk.Label(self.dim_fields_frame, text="Longueur (cm):").grid(row=1, column=0, sticky='w')
            self.longueur_entry = ttk.Entry(self.dim_fields_frame)
            self.longueur_entry.grid(row=1, column=1, padx=5, pady=2)

            ttk.Label(self.dim_fields_frame, text="Largeur (cm):").grid(row=2, column=0, sticky='w')
            self.largeur_entry = ttk.Entry(self.dim_fields_frame)
            self.largeur_entry.grid(row=2, column=1, padx=5, pady=2)
        else:
            ttk.Label(self.dim_fields_frame, text="Diamètre (cm):").grid(row=1, column=0, sticky='w')
            self.diametre_entry = ttk.Entry(self.dim_fields_frame)
            self.diametre_entry.grid(row=1, column=1, padx=5, pady=2)

    def create_materials_tab(self):
        # Béton
        beton_frame = ttk.LabelFrame(self.tab_materials, text="Béton")
        beton_frame.pack(padx=10, pady=5, fill="x")

        ttk.Label(beton_frame, text="Fc28 (MPa):").grid(row=0, column=0, sticky="w")
        self.fc28_entry = ttk.Entry(beton_frame)
        self.fc28_entry.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(beton_frame, text="γ béton:").grid(row=1, column=0, sticky="w")
        self.gamma_beton_entry = ttk.Entry(beton_frame)
        self.gamma_beton_entry.grid(row=1, column=1, padx=5, pady=2)

        # Acier
        acier_frame = ttk.LabelFrame(self.tab_materials, text="Acier")
        acier_frame.pack(padx=10, pady=5, fill="x")

        ttk.Label(acier_frame, text="Fe longitudinal (MPa):").grid(
            row=0, column=0, sticky="w"
        )
        self.fe_long_entry = ttk.Entry(acier_frame)
        self.fe_long_entry.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(acier_frame, text="Fe transversal (MPa):").grid(
            row=1, column=0, sticky="w"
        )
        self.fe_trans_entry = ttk.Entry(acier_frame)
        self.fe_trans_entry.grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(acier_frame, text="γ acier:").grid(row=2, column=0, sticky="w")
        self.gamma_acier_entry = ttk.Entry(acier_frame)
        self.gamma_acier_entry.grid(row=2, column=1, padx=5, pady=2)

    def create_standards_tab(self):
        standards_frame = ttk.LabelFrame(self.tab_standards, text="Normes de calcul")
        standards_frame.pack(padx=10, pady=5, fill="both", expand=True)

        self.norme_var = tk.StringVar()
        normes = ["BAEL 91", "Eurocode 2"]

        ttk.Combobox(
            standards_frame,
            textvariable=self.norme_var,
            values=normes,
            state="readonly",
        ).pack(padx=10, pady=10)

    def create_solicitations_tab(self):
        solicitation_frame = ttk.LabelFrame(
            self.tab_solicitations, text="Type de sollicitation"
        )
        solicitation_frame.pack(padx=10, pady=5, fill="both", expand=True)

        self.solicitation_var = tk.StringVar()
        solicitations = ["Compression", "Traction", "Flexion composée"]

        for i, solicitation in enumerate(solicitations):
            ttk.Radiobutton(
                solicitation_frame,
                text=solicitation,
                variable=self.solicitation_var,
                value=solicitation,
            ).pack(anchor="w", padx=10, pady=2)

    def run_calculation(self):
        # À implémenter plus tard
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = PoteauCalculatorApp(root)
    root.mainloop()
