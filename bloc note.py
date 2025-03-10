#appli simple d'un bloc note

import tkinter as tk
import os
from tkinter import ttk, filedialog, messagebox

def creer_fichier(event = None): #event = None pour accepter que la fonction soit associée à un raccourci clavier
    onglet = ttk.Frame(notebook)
    text_area = tk.Text(onglet, wrap="word", undo=True)
    text_area.pack(expand=1, fill="both")

    notebook.add(onglet, text = f"Document {len(notebook.tabs())+1}") # Numérote les onglets
    notebook.select(onglet)

def ouvrir_fichier(event = None): #event = None pour accepter que la fonction soit associée à un raccourci clavier
    fichier = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")])
    if fichier:
        with open(fichier, "r", encoding="utf-8") as f:
            contenu = f.read()
        
        onglet = ttk.Frame(notebook)
        text_area = tk.Text(onglet, wrap="word", undo=True)
        text_area.pack(expand=1, fill="both")
        text_area.insert("1.0", contenu)

        notebook.add(onglet, text = os.path.basename(fichier))
        notebook.select(onglet)

def enregistrer_fichier(event = None): #event = None pour accepter que la fonction soit associée à un raccourci clavier
    onglet_actif = notebook.nametowidget(notebook.select())
    text_area = onglet_actif.winfo_children()[0]

    fichier = filedialog.asksaveasfilename(defaultextension=".txt",
                                           filetypes=[("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")])
    if fichier:
        with open(fichier, "w", encoding="utf-8") as f:
            f.write(text_area.get("1.0", "end-1c"))  # Sauvegarde le contenu
        notebook.tab(onglet_actif, os.path.basename(fichier))  # Met à jour le nom de l'onglet

def annuler_action():
    onglet_actif = notebook.nametowidget(notebook.select())
    text_area = onglet_actif.winfo_children()[0]
    text_area.edit_undo()  # Annule la dernière action

def retablir_action():
    onglet_actif = notebook.nametowidget(notebook.select())
    text_area = onglet_actif.winfo_children()[0]
    text_area.edit_redo()  # Rétablit l'action annulée

def copier_texte():
    onglet_actif = notebook.nametowidget(notebook.select())
    text_area = onglet_actif.winfo_children()[0]
    # Copier le texte sélectionné
    text_area.event_generate("<<Copy>>")

def coller_texte():
    onglet_actif = notebook.nametowidget(notebook.select())
    text_area = onglet_actif.winfo_children()[0]
    # Copier le texte sélectionné
    text_area.event_generate("<<Paste>>")

def couper_texte():
    onglet_actif = notebook.nametowidget(notebook.select())
    text_area = onglet_actif.winfo_children()[0]
    # Copier le texte sélectionné
    text_area.event_generate("<<Cut>>")

#======================================================================================================
root = tk.Tk()
root.geometry("500x500")

# Création du Notebook (ensemble d'onglets)
notebook = ttk.Notebook(root)
notebook.pack(expand=1, fill="both")  

# Créer un premier onglet par défaut
onglet = creer_fichier()

# Raccourci clavier
root.bind("<Control-s>", enregistrer_fichier)
root.bind("<Control-n>", creer_fichier)
root.bind("<Control-o>", ouvrir_fichier)

# Menu du bloc note
menubar = tk.Menu(root)

menu1_fichier = tk.Menu(menubar, tearoff = 0)
menubar.add_cascade(label="Fichier", menu = menu1_fichier)
menu1_fichier.add_command(label="Nouveau fichier (Ctrl N)", command = creer_fichier)
menu1_fichier.add_command(label="Ouvrir (Ctrl O)", command = ouvrir_fichier)
menu1_fichier.add_command(label="Enregistrer (Ctrl S)", command = enregistrer_fichier)
menu1_fichier.add_separator()
menu1_fichier.add_command(label="Quitter", command = root.quit)

menu2_fichier = tk.Menu(menubar, tearoff = 0)
menubar.add_cascade(label="Editer", menu = menu2_fichier)
menu2_fichier.add_command(label="Annuler (Ctrl Z)", command = annuler_action)
menu2_fichier.add_command(label="Rétablir (Ctrl Y)", command = retablir_action)
menu1_fichier.add_separator()
menu2_fichier.add_command(label="Copier (Ctrl C)", command = copier_texte)
menu2_fichier.add_command(label="Coller (Ctrl V)", command = coller_texte)
menu2_fichier.add_command(label="Couper (Ctrl X)", command = couper_texte)

# Ajout du menu à la fenêtre
root.config(menu = menubar)

root.mainloop()