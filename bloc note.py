"""
Application d'un bloc note simple qui permet:
- De créer un nouveau fichier
- D'ouvrir un fichier existant
- D'enregistrer un fichier
- D'éditer le texte en copiant/collant/coupant le texte et en annulant/rétablissant une action
- De fermer un onglet via le menu

Améliorations possibles:
- Fermer les onglet via une croix à côté de leurs titres (essayé mais echec)
- Ajout d'une barre de scroll verticale et horizontale
"""
import tkinter as tk
import os
from tkinter import ttk, filedialog, messagebox
from tkinter.ttk import *

# Dictionnaire pour stocker les chemins des fichiers ouverts
fichiers_ouverts = {}

def marquer_comme_modifie(event=None):
    #Ajoute une * à l'onglet si le texte est modifié
    onglet_actif = notebook.nametowidget(notebook.select())
    text_actif = onglet_actif.winfo_children()[0]

    if text_actif.edit_modified():  # Vérifie si le texte a été modifié
        titre = notebook.tab(onglet_actif, "text")
        if not titre.endswith("*"):
            notebook.tab(onglet_actif, text=titre + " *")

        text_actif.edit_modified(False)

"""================================================================================================
                                              FICHIER
================================================================================================"""

def creer_fichier(event=None): #event = None pour accepter que la fonction soit associée à un raccourci clavier
    onglet = ttk.Frame(notebook)
    text_area = tk.Text(onglet, wrap="word", undo=True)
    text_area.pack(expand=1, fill="both")

    #ajouter_fermeture_onglet()
    notebook.add(onglet, text = f"Document {len(notebook.tabs())+1}") # Numérote les onglets
    notebook.select(onglet)

    # Ajouter le fichier au dictionnaire avec un chemin vide (nouveau fichier)
    fichiers_ouverts[onglet] = None 
    
    text_area.bind("<<Modified>>", marquer_comme_modifie)  # Détecte les modifications

def ouvrir_fichier(event=None): #event = None pour accepter que la fonction soit associée à un raccourci clavier
    fichier = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")])
    if fichier:
        with open(fichier, "r", encoding="utf-8") as f:
            contenu = f.read()
        
        onglet = ttk.Frame(notebook)
        text_area = tk.Text(onglet, wrap="word", undo=True)
        text_area.pack(expand=1, fill="both")
        text_area.insert("1.0", contenu)
        # Permet de faire en sorte que l'application ne considère pas le recopiage du contenu du fichier comme une modification
        text_area.edit_modified(False)

        #ajouter_fermeture_onglet()
        notebook.add(onglet, text = f"{os.path.basename(fichier)}")
        notebook.select(onglet)

        # Stocker le chemin du fichier
        fichiers_ouverts[onglet] = fichier  

        text_area.bind("<<Modified>>", marquer_comme_modifie)  # Détecte les modifications

def enregistrer_sous_fichier(event=None): #event = None pour accepter que la fonction soit associée à un raccourci clavier
    onglet_actif = notebook.nametowidget(notebook.select())
    text_area = onglet_actif.winfo_children()[0]

    fichier = filedialog.asksaveasfilename(defaultextension=".txt",
                                           filetypes=[("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")])
    if fichier:
        with open(fichier, "w", encoding="utf-8") as f:
            f.write(text_area.get("1.0", "end-1c"))  # Sauvegarde le contenu

        #ajouter_fermeture_onglet()

        notebook.tab(onglet_actif, text=os.path.basename(fichier))  # Enlève si il y a eu des modifications *

        fichiers_ouverts[onglet_actif] = fichier  # Stocke le chemin du fichier

def enregistrer_fichier(event=None):
    onglet_actif = notebook.nametowidget(notebook.select())
    text_area = onglet_actif.winfo_children()[0]

    fichier = fichiers_ouverts.get(onglet_actif)  # Récupérer le chemin du fichier
    if fichier:
        with open(fichier, "w", encoding="utf-8") as f:
            f.write(text_area.get("1.0", "end-1c"))  # Sauvegarde du contenu

        notebook.tab(onglet_actif, text=os.path.basename(fichier))  # Enlève * si il y a eu des modifications

    else:
        enregistrer_sous_fichier()  # Si pas encore enregistré, demander un nom

def quitter_application(event=None):
    documents_non_enregistres = any(
        notebook.tab(onglet, "text").endswith("*") for onglet in notebook.winfo_children()
    )

    # s'il existe au moins 1 documents qui n'est pas enregistré
    if documents_non_enregistres:
        reponse = messagebox.askquestion(
            "Quitter", "Un ou plusieurs documents ne sont pas enregistrés. Voulez-vous vraiment quitter ?",
            icon="warning"
        )
        if reponse == "no":
            return # Empêche la fermeture de l'application

    root.quit() # Quitte l'application si tout est enregistré ou si l'utilisateur accepte


"""================================================================================================
                                              EDITER
================================================================================================"""

def fermer_onglet(event=None):
    onglet_actif = notebook.nametowidget(notebook.select())
    titre = notebook.tab(onglet_actif, "text")

    # Si le document n'est pas enregistré
    if titre.endswith("*"):
        reponse = messagebox.askquestion("Form", "Le document n'est pas enregistré, voulez-vous continuer?", icon ='warning')
        if reponse == "no":
            return #arrête la fonction pour que l'onglet ne se ferme pas

    # Supprime aussi du dictionnaire des fichiers ouverts (évite d'éventuelles erreurs)
    if onglet_actif in fichiers_ouverts:
        del fichiers_ouverts[onglet_actif]

    # Pour chaque onglet, ferme l'onglet sélectionné
    for item in notebook.winfo_children():
        if str(item) == (notebook.select()):
            item.destroy()
            break  #Necessaire sinon la boucle supprime tous les onglets

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
    # Coller le texte sélectionné
    text_area.event_generate("<<Paste>>")

def couper_texte():
    onglet_actif = notebook.nametowidget(notebook.select())
    text_area = onglet_actif.winfo_children()[0]
    # Couper le texte sélectionné
    text_area.event_generate("<<Cut>>")

"""================================================================================================
                                              MAIN
================================================================================================"""

root = tk.Tk()
root.geometry("800x500")
root.title("Bloc note")

# Création du Notebook (ensemble d'onglets)
notebook = ttk.Notebook(root)
notebook.pack(expand=1, fill="both")  

# Créer un premier onglet par défaut
onglet = creer_fichier()

# Raccourci clavier
root.bind("<Control-s>", enregistrer_fichier)
root.bind("<Control-Shift-S>", enregistrer_sous_fichier)
root.bind("<Control-n>", creer_fichier)
root.bind("<Control-o>", ouvrir_fichier)
root.bind("<Control-f>", fermer_onglet)
root.bind("<Control-q>", quitter_application)

# Menu du bloc note
menubar = tk.Menu(root)

menu1_fichier = tk.Menu(menubar, tearoff = 0)
menubar.add_cascade(label="Fichier", menu = menu1_fichier)
menu1_fichier.add_command(label="Nouveau fichier (Ctrl N)", command = creer_fichier)
menu1_fichier.add_command(label="Ouvrir (Ctrl O)", command = ouvrir_fichier)
menu1_fichier.add_command(label="Enregistrer sous (Ctrl Shift S)", command = enregistrer_sous_fichier)
menu1_fichier.add_command(label="Enregistrer (Ctrl S)", command = enregistrer_fichier)
menu1_fichier.add_separator()
menu1_fichier.add_command(label="Quitter (Ctrl Q)", command = quitter_application)

menu2_fichier = tk.Menu(menubar, tearoff = 0)
menubar.add_cascade(label="Editer", menu = menu2_fichier)
menu2_fichier.add_command(label="Supprimer l'onglet actif (Ctrl F)", command = fermer_onglet)
menu2_fichier.add_command(label="Annuler (Ctrl Z)", command = annuler_action)
menu2_fichier.add_command(label="Rétablir (Ctrl Y)", command = retablir_action)
menu1_fichier.add_separator()
menu2_fichier.add_command(label="Copier (Ctrl C)", command = copier_texte)
menu2_fichier.add_command(label="Coller (Ctrl V)", command = coller_texte)
menu2_fichier.add_command(label="Couper (Ctrl X)", command = couper_texte)

# Ajout du menu à la fenêtre
root.config(menu = menubar)

root.mainloop()
