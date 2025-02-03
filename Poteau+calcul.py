import tkinter as tk
from tkinter import ttk
import math
import threading
import time


class PoteauCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculateur de Poteaux en Béton Armé")

        # Configuration du style
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Error.TEntry", fieldbackground="#FFC0C0")

        # Configuration de la mise en page
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill="both", expand=True)

        # Canvas pour les schémas
        self.canvas = tk.Canvas(self.main_frame, width=300, height=400, bg="white")
        self.canvas.pack(side="right", fill="y", padx=10, pady=10)

        # Création des onglets
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(side="left", expand=1, fill="both", padx=10, pady=10)

        # Création des onglets et composants
        self.create_tabs()
        self.create_navigation_buttons()
        self.create_results_tab()

        # Dessin initial
        self.update_schema()

    def create_tabs(self):
        self.tabs = {
            "dimensions": ttk.Frame(self.notebook),
            "materials": ttk.Frame(self.notebook),
            "standards": ttk.Frame(self.notebook),
            "solicitations": ttk.Frame(self.notebook),
        }

        for name, frame in self.tabs.items():
            self.notebook.add(frame, text=self.get_tab_title(name))

        self.create_dimensions_tab()
        self.create_materials_tab()
        self.create_standards_tab()
        self.create_solicitations_tab()

    def get_tab_title(self, name):
        titles = {
            "dimensions": "📏 Dimensions",
            "materials": "🧱 Matériaux",
            "standards": "📜 Normes",
            "solicitations": "⚡ Sollicitations",
        }
        return titles[name]

    def create_navigation_buttons(self):
        btn_frame = ttk.Frame(self.main_frame)
        btn_frame.pack(side="bottom", pady=10)

        self.btn_prev = ttk.Button(btn_frame, text="Précédent", command=self.prev_tab)
        self.btn_prev.pack(side="left", padx=5)

        self.btn_next = ttk.Button(btn_frame, text="Suivant", command=self.next_tab)
        self.btn_next.pack(side="left", padx=5)

        self.btn_calculate = ttk.Button(
            btn_frame, text="Lancer le calcul", command=self.start_calculation
        )
        self.btn_calculate.pack(side="left", padx=5)

        self.update_navigation_buttons()

    def create_results_tab(self):
        self.results_tab = ttk.Frame(self.notebook)
        self.results_content = ttk.Frame(self.results_tab)
        self.loading_label = ttk.Label(self.results_tab, text="Calcul en cours...")

    def create_dimensions_tab(self):
        # Section forme du poteau
        shape_frame = ttk.LabelFrame(self.tabs["dimensions"], text="Forme du poteau")
        shape_frame.pack(padx=10, pady=5, fill="x")

        self.shape_var = tk.StringVar(value="rectangulaire")
        ttk.Radiobutton(
            shape_frame,
            text="Rectangulaire",
            variable=self.shape_var,
            value="rectangulaire",
            command=self.update_dimension_fields,
        ).pack(side="left", padx=5)
        ttk.Radiobutton(
            shape_frame,
            text="Circulaire",
            variable=self.shape_var,
            value="circulaire",
            command=self.update_dimension_fields,
        ).pack(side="left", padx=5)

        # Ajout de l'enrobage
        enrobage_frame = ttk.Frame(self.tabs["dimensions"])
        enrobage_frame.pack(padx=10, pady=5, fill="x")

        ttk.Label(enrobage_frame, text="Enrobage (cm):").grid(row=0, column=0, sticky="w")
        self.enrobage_entry = ttk.Entry(enrobage_frame)
        self.enrobage_entry.grid(row=0, column=1, padx=5, pady=2)
        # Conteneur pour les champs liés aux dimensions de la section
        self.dim_fields_frame = ttk.Frame(self.tabs["dimensions"])
        self.dim_fields_frame.pack(padx=10, pady=5, fill="x")

        # Hauteur du poteau
        ttk.Label(self.dim_fields_frame, text="Hauteur du poteau (cm):").grid(
            row=0, column=0, sticky="w"
        )
        self.hauteur_entry = ttk.Entry(self.dim_fields_frame)
        self.hauteur_entry.grid(row=0, column=1, padx=5, pady=2)



        # Création dynamique d'autres champs (longueur, largeur ou diamètre) selon la forme
        self.update_dimension_fields()

        # ---- Zone dédiée au choix de la longueur de flambement ----
        # On crée un conteneur unique pour la zone flambement, le bouton et le résultat
        self.flambement_zone = ttk.Frame(self.tabs["dimensions"])
        self.flambement_zone.pack(padx=10, pady=5, fill="x")

        # Cadre pour le choix du facteur de flambement
        flambement_frame = ttk.LabelFrame(self.flambement_zone, text="Longueur de flambement (lf)")
        flambement_frame.pack(fill="x")
        self.l0_option_var = tk.StringVar(value="l0")
        options = [
            ("l0", "l0"),
            ("0.7 * l0", "0.7*l0"),
            ("0.5 * l0", "0.5*l0"),
            ("2 * l0", "2*l0")
        ]
        for text, mode in options:
            ttk.Radiobutton(
                flambement_frame,
                text=text,
                variable=self.l0_option_var,
                value=mode
            ).pack(side="left", padx=5)

        # Bouton pour calculer lf et label pour afficher le résultat
        # Ceux-ci sont créés une seule fois dans le conteneur flambement_zone
        self.calc_button = ttk.Button(self.flambement_zone, text="Calculer lf", command=self.update_flambement)
        self.calc_button.pack(pady=5)

        self.lf_label = ttk.Label(self.flambement_zone, text="lf = ?")
        self.lf_label.pack(pady=5)

    def update_flambement(self):
        # Récupération de la hauteur du poteau en cm et conversion en m
        try:
            h_col_cm = float(self.hauteur_entry.get())
            h_col = h_col_cm / 100.0
        except ValueError:
            self.lf_label.config(text="Erreur : Hauteur invalide")
            return

        # Calcul de lf en fonction du choix de l'utilisateur
        choice = self.l0_option_var.get()
        if choice == "l0":
            lf = h_col
        elif choice == "0.7*l0":
            lf = 0.7 * h_col
        elif choice == "0.5*l0":
            lf = 0.5 * h_col
        elif choice == "2*l0":
            lf = 2 * h_col
        else:
            lf = h_col  # Valeur par défaut

        # Stockage de lf pour utilisation ultérieure
        self.lf = lf

        # Calcul de l'élancement λ = lf / i_min
        shape = self.shape_var.get()
        try:
            if shape == "rectangulaire":
                # Pour un poteau rectangulaire
                d_cm = float(self.longueur_entry.get())
                b_cm = float(self.largeur_entry.get())
                d = d_cm / 100.0  # conversion en m
                b = b_cm / 100.0
                i_min = min(d, b) / (12 ** 0.5)
            elif shape == "circulaire":
                # Pour un poteau circulaire
                d_cm = float(self.diametre_entry.get())
                d = d_cm / 100.0  # conversion en m
                i_min = d / 4.0
            else:
                i_min = 0
        except Exception as e:
            self.lf_label.config(text=f"Erreur dimensions section : {str(e)}")
            return

        # Si i_min est nul, on ne peut pas calculer l'élancement
        if i_min <= 0:
            elancement = float('inf')
        else:
            elancement = lf / i_min

        # Stockage de l'élancement pour utilisation ultérieure
        self.elancement = elancement

        # Affichage des deux résultats dans un seul label
        self.lf_label.config(text=f"lf = {lf:.2f} m, λ = {elancement:.2f}")
    def update_dimension_fields(self):
        # Supprime les widgets dynamiques précédents
        for widget in self.dim_fields_frame.winfo_children()[2:]:
            widget.destroy()

        if self.shape_var.get() == "rectangulaire":
            ttk.Label(self.dim_fields_frame, text="Longueur (cm):").grid(
                row=1, column=0, sticky="w"
            )
            self.longueur_entry = ttk.Entry(self.dim_fields_frame)
            self.longueur_entry.grid(row=1, column=1, padx=5, pady=2)

            ttk.Label(self.dim_fields_frame, text="Largeur (cm):").grid(
                row=2, column=0, sticky="w"
            )
            self.largeur_entry = ttk.Entry(self.dim_fields_frame)
            self.largeur_entry.grid(row=2, column=1, padx=5, pady=2)
        else:
            ttk.Label(self.dim_fields_frame, text="Diamètre (cm):").grid(
                row=1, column=0, sticky="w"
            )
            self.diametre_entry = ttk.Entry(self.dim_fields_frame)
            self.diametre_entry.grid(row=1, column=1, padx=5, pady=2)

        self.update_schema()

    def create_materials_tab(self):
        # Béton
        beton_frame = ttk.LabelFrame(self.tabs["materials"], text="Béton")
        beton_frame.pack(padx=10, pady=5, fill="x")

        ttk.Label(beton_frame, text="Fc28 (MPa):").grid(row=0, column=0, sticky="w")
        self.fc28_entry = ttk.Entry(beton_frame)
        self.fc28_entry.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(beton_frame, text="γ béton:").grid(row=1, column=0, sticky="w")
        self.gamma_beton_entry = ttk.Entry(beton_frame)
        self.gamma_beton_entry.grid(row=1, column=1, padx=5, pady=2)

        # Acier
        acier_frame = ttk.LabelFrame(self.tabs["materials"], text="Acier")
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
        standards_frame = ttk.LabelFrame(
            self.tabs["standards"], text="Normes de calcul"
        )
        standards_frame.pack(padx=10, pady=5, fill="both", expand=True)

        self.norme_var = tk.StringVar()
        ttk.Combobox(
            standards_frame,
            textvariable=self.norme_var,
            values=["BAEL 91", "Eurocode 2"],
            state="readonly",
        ).pack(padx=10, pady=10)

    def create_solicitations_tab(self):
        solicitation_frame = ttk.LabelFrame(
            self.tabs["solicitations"], text="Type de sollicitation"
        )
        solicitation_frame.pack(padx=10, pady=5, fill="both", expand=True)

        # Choix du type de sollicitation
        self.solicitation_var = tk.StringVar(value="Compression")
        for solicitation in ["Compression", "Traction", "Flexion composée"]:
            ttk.Radiobutton(
                solicitation_frame,
                text=solicitation,
                variable=self.solicitation_var,
                value=solicitation,
                command=self.update_load_fields,
            ).pack(anchor="w", padx=10, pady=2)

        # Combobox pour le type de calcul (ELS ou ELU)
        ttk.Label(solicitation_frame, text="Type de calcul:").pack(
            anchor="w", padx=10, pady=(10, 2)
        )
        self.calculation_type_var = tk.StringVar(value="ELS")
        calc_type_cb = ttk.Combobox(
            solicitation_frame,
            textvariable=self.calculation_type_var,
            values=["ELS", "ELU"],
            state="readonly",
        )
        calc_type_cb.pack(anchor="w", padx=10, pady=(0, 10))

        # Cadre pour les chargements
        self.load_frame = ttk.LabelFrame(solicitation_frame, text="Chargements")
        self.load_frame.pack(padx=10, pady=5, fill="both", expand=True)

        # Champs pour g et q
        ttk.Label(self.load_frame, text="g (kN):").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.g_entry = ttk.Entry(self.load_frame)
        self.g_entry.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(self.load_frame, text="q (kN):").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.q_entry = ttk.Entry(self.load_frame)
        self.q_entry.grid(row=1, column=1, padx=5, pady=2)

        # Champ pour le moment fléchissant (affiché uniquement en flexion composée)
        self.moment_label = ttk.Label(self.load_frame, text="Moment fléchissant (kN.m):")
        self.moment_entry = ttk.Entry(self.load_frame)

        self.update_load_fields()  # Mise à jour initiale des champs

    def update_load_fields(self):
        # Affiche ou masque le champ du moment selon la sollicitation
        if self.solicitation_var.get() == "Flexion composée":
            self.moment_label.grid(row=2, column=0, sticky="w", padx=5, pady=2)
            self.moment_entry.grid(row=2, column=1, padx=5, pady=2)
        else:
            self.moment_label.grid_forget()
            self.moment_entry.grid_forget()

    def update_schema(self):
        self.canvas.delete("all")
        try:
            h = float(self.hauteur_entry.get()) if self.hauteur_entry.get() else 0
        except:
            h = 0

        if self.shape_var.get() == "rectangulaire":
            self.draw_rectangular_schema(h)
        else:
            self.draw_circular_schema(h)

    def draw_rectangular_schema(self, height):
        scale = 0.4  # Facteur d'échelle pour visualisation
        x, y = 50, 50

        # Élévation
        self.canvas.create_rectangle(x, y, x + 100, y + height * scale, outline="black")
        self.add_dimension_arrow(x - 20, y, x - 20, y + height * scale, f"{height} cm")

        # Coupe transversale
        try:
            l = float(self.longueur_entry.get())
            w = float(self.largeur_entry.get())
        except:
            l, w = 0, 0

        self.canvas.create_rectangle(
            200, 200, 200 + l * scale, 200 + w * scale, outline="black"
        )
        self.canvas.create_text(200 + l * scale / 2, 190, text=f"Longueur: {l} cm")
        self.canvas.create_text(
            200 + l * scale / 2, 210 + w * scale, text=f"Largeur: {w} cm"
        )
        # Ajout de l'enrobage
        try:
            enrobage = float(self.enrobage_entry.get())
        except:
            enrobage = 0

        # Dessin de l'enrobage
        self.canvas.create_rectangle(
            x + enrobage * 10, y + enrobage * 10,
            x + 100 - enrobage * 10, y + height * scale - enrobage * 10,
            outline="red", dash=(4, 2)
        )
    def draw_circular_schema(self, height):
        scale = 0.4
        x, y = 50, 50

        # Élévation
        self.canvas.create_rectangle(x, y, x + 100, y + height * scale, outline="black")
        self.add_dimension_arrow(x - 20, y, x - 20, y + height * scale, f"{height} cm")

        # Coupe transversale
        try:
            d = float(self.diametre_entry.get())
        except:
            d = 0

        self.canvas.create_oval(
            200 - d * scale / 2,
            200 - d * scale / 2,
            200 + d * scale / 2,
            200 + d * scale / 2,
            outline="black",
        )
        self.canvas.create_text(200, 210 + d * scale / 2, text=f"⌀ {d} cm")
        # Ajout de l'enrobage
        try:
            enrobage = float(self.enrobage_entry.get())
        except:
            enrobage = 0

        # Dessin de l'enrobage
        self.canvas.create_oval(
            200 - (d * scale / 2 - enrobage * 10),
            200 - (d * scale / 2 - enrobage * 10),
            200 + (d * scale / 2 - enrobage * 10),
            200 + (d * scale / 2 - enrobage * 10),
            outline="red", dash=(4, 2)
        )
    def add_dimension_arrow(self, x1, y1, x2, y2, text):
        self.canvas.create_line(x1, y1, x1, y2, arrow=tk.BOTH)
        self.canvas.create_text(x1 - 10, (y1 + y2) / 2, text=text, angle=90)

    def next_tab(self):
        current = self.notebook.index("current")
        if current < len(self.notebook.tabs()) - 1:
            self.notebook.select(current + 1)
        self.update_navigation_buttons()
        self.update_schema()

    def prev_tab(self):
        current = self.notebook.index("current")
        if current > 0:
            self.notebook.select(current - 1)
        self.update_navigation_buttons()
        self.update_schema()

    def update_navigation_buttons(self):
        current = self.notebook.index("current")
        self.btn_prev["state"] = "disabled" if current == 0 else "enabled"
        self.btn_next["state"] = (
            "disabled" if current == len(self.notebook.tabs()) - 1 else "enabled"
        )

    def start_calculation(self):
        error_fields = self.validate_inputs()

        if error_fields:
            self.show_error("Champs invalides détectés", error_fields)
            return

        self.prepare_results_tab()
        threading.Thread(target=self.run_calculation).start()

    def prepare_results_tab(self):
        if self.results_tab not in self.notebook.tabs():
            self.notebook.add(self.results_tab, text="📊 Résultats")
        self.notebook.select(self.results_tab)
        self.loading_label.pack(pady=50)

    def validate_inputs(self):
        error_fields = []

        # Validation dimensions
        if not self.validate_number(self.hauteur_entry, min_val=0):
            error_fields.append("hauteur")

        if self.shape_var.get() == "rectangulaire":
            if not self.validate_number(self.longueur_entry, min_val=0):
                error_fields.append("longueur")
            if not self.validate_number(self.largeur_entry, min_val=0):
                error_fields.append("largeur")
        else:
            if not self.validate_number(self.diametre_entry, min_val=0):
                error_fields.append("diametre")

        # Validation matériaux
        material_fields = {
            "fc28": self.fc28_entry,
            "gamma_beton": self.gamma_beton_entry,
            "fe_long": self.fe_long_entry,
            "fe_trans": self.fe_trans_entry,
            "gamma_acier": self.gamma_acier_entry,
        }

        for field, entry in material_fields.items():
            if not self.validate_number(entry, min_val=0.1):
                error_fields.append(field)

        # Validation chargements (g et q)
        if not self.validate_number(self.g_entry, min_val=0):
            error_fields.append("g")
        if not self.validate_number(self.q_entry, min_val=0):
            error_fields.append("q")

        # Validation moment fléchissant en cas de flexion composée
        if self.solicitation_var.get() == "Flexion composée":
            if not self.validate_number(self.moment_entry, min_val=0):
                error_fields.append("moment")

        if error_fields:
            self.highlight_error_fields(error_fields)

        return error_fields

    def validate_number(self, entry, min_val=0):
        try:
            value = float(entry.get())
            return value >= min_val
        except:
            return False

    def highlight_error_fields(self, fields):
        field_mapping = {
            "hauteur": self.hauteur_entry,
            "longueur": self.longueur_entry if hasattr(self, "longueur_entry") else None,
            "largeur": self.largeur_entry if hasattr(self, "largeur_entry") else None,
            "diametre": self.diametre_entry if hasattr(self, "diametre_entry") else None,
            "fc28": self.fc28_entry,
            "gamma_beton": self.gamma_beton_entry,
            "fe_long": self.fe_long_entry,
            "fe_trans": self.fe_trans_entry,
            "gamma_acier": self.gamma_acier_entry,
            "g": self.g_entry,
            "q": self.q_entry,
            "moment": self.moment_entry,
            "enrobage": self.enrobage_entry,
        }

        for field in fields:
            if widget := field_mapping.get(field):
                widget.config(style="Error.TEntry")
                self.root.after(5000, lambda w=widget: w.config(style="TEntry"))

    def run_calculation(self):
        time.sleep(2)  # Simulation de calcul

        try:
            # Calcul de la section transversale
            h = float(self.hauteur_entry.get()) / 100
            if self.shape_var.get() == "rectangulaire":
                l = float(self.longueur_entry.get()) / 100
                w = float(self.largeur_entry.get()) / 100
                section = l * w
            else:
                d = float(self.diametre_entry.get()) / 100
                section = math.pi * (d / 2) ** 2

            # Chargements
            g_val = float(self.g_entry.get())
            q_val = float(self.q_entry.get())
            calc_type = self.calculation_type_var.get()

            if calc_type == "ELS":
                N = g_val + q_val  # Nser = g + q
            else:  # ELU
                N = 1.35 * g_val + 1.5 * q_val  # Nu = 1.35g + 1.5q

            solicitation = self.solicitation_var.get()

            if solicitation in ["Compression", "Traction"]:
                result_text = (
                    f"Section transversale: {section:.2f} m²\n"
                    f"Effort Normal calculé: {N:.2f} kN\n"
                    f"(Utilisation de Nᵤ pour ELU et Nₛₑᵣ pour ELS)"
                )
            elif solicitation == "Flexion composée":
                M_val = float(self.moment_entry.get())
                result_text = (
                    f"Section transversale: {section:.2f} m²\n"
                    f"Effort Normal calculé: {N:.2f} kN\n"
                    f"Moment fléchissant: {M_val:.2f} kN.m\n"
                    f"(Utiliser Nₛₑᵣ et M ou Nᵤ et M selon la méthode)"
                )
            else:
                result_text = "Méthode de sollicitation non reconnue."

            self.root.after(0, self.show_results, result_text)
        except Exception as e:
            self.root.after(0, self.show_error, f"Erreur de calcul : {str(e)}")

    def show_results(self, result_text):
        self.loading_label.pack_forget()

        for widget in self.results_content.winfo_children():
            widget.destroy()

        self.results_content.pack(fill="both", expand=True)

        ttk.Label(
            self.results_content, text="Résultats du calcul", font=("Arial", 14, "bold")
        ).pack(pady=10)

        ttk.Label(
            self.results_content,
            text=result_text,
            font=("Arial", 12),
        ).pack(pady=5)

    def show_error(self, message, fields=None):
        self.loading_label.pack_forget()

        for widget in self.results_content.winfo_children():
            widget.destroy()

        self.results_content.pack(fill="both", expand=True)

        ttk.Label(
            self.results_content,
            text=f"⛔ Erreur : {message}",
            foreground="red",
            font=("Arial", 12, "bold"),
        ).pack(pady=10)

        if fields:
            ttk.Label(
                self.results_content,
                text="Champs invalides : " + ", ".join(fields),
                foreground="darkred",
            ).pack()

        ttk.Button(
            self.results_content,
            text="Corriger les entrées",
            command=self.retry_calculation,
        ).pack(pady=10)

    def retry_calculation(self):
        self.notebook.hide(self.results_tab)
        self.notebook.select(self.tabs["dimensions"])

# calcul
#compression simple
def calcul_compression(standard, N, section, fc28, fe, gamma_beton, gamma_acier, lf, enrobage):
    if standard == "BAEL 91":
        # BAEL 91 Art. B.8.4
        lambda_lim = 35
        Br = (section[0] - 2 * enrobage) * (section[1] - 2 * enrobage)  # Section réduite
        alpha = min(0.85 / (1 + 0.2 * (lf / 1000) ** 2), 0.81)  # Coefficient de flambement

        A_min = max(4 * section * 1e-4, 0.2 * N * 1e3 / fe)  # cm²
        A_calc = (N * 1e3 / 0.9 - Br * fc28 / 1.5) / (fe / 1.15)

    elif standard == "Eurocode 2":
        # EN 1992-1-1 §6.1
        Ac = section * 1e4  # cm²
        Nrd = 0.8 * Ac * (0.85 * fc28 / gamma_beton) * (1 - (lf / (200 * math.sqrt(Ac))) ** 2)
        A_calc = max((N * 1e3 - Nrd) / (fe / gamma_acier), 0)

    return A_calc

# Tarction
def calcul_traction(standard, N, fe, gamma_acier):
    # Le béton ne participe pas
    if standard == "BAEL 91":
        A = N * 1e3 / (fe / 1.15)
    elif standard == "Eurocode 2":
        A = N * 1e3 / (fe / gamma_acier)

    return A

#Flexion compose






if __name__ == "__main__":
    root = tk.Tk()
    app = PoteauCalculatorApp(root)
    root.mainloop()
