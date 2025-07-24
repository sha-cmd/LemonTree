#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Programme Joyeux Noël avec interface graphique
Fonctionnalités:
- Charger une clé GPG privée
- Déchiffrer et servir un fichier HTML remark.js
- Lire un fichier MP3
- Compilable avec PyInstaller
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import queue
import pygame
import hashlib
import os
import sys
from PIL import Image, ImageTk


class JoyeuxNoelApp:
    def __init__(self, root):
        self.root = root
        self.setup_variables()
        self.setup_window()
        self.create_widgets()
        self.server_thread = None
        self.music_playing = False

    def setup_window(self):
        self.root.title(" Joyeux Noël ")
        self.root.geometry("500x400")
        self.root.configure(bg="#2c5530")  # Vert sapin
        self.root.resizable(False, False)
        self.root.config(cursor="heart")
        self.root.iconbitmap(self.fav_file_path)

        # Centrer la fenêtre
        self.center_window()

    def center_window(self):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.root.winfo_screenheight() // 2) - (400 // 2)
        self.root.geometry(f"500x400+{x}+{y}")

    def setup_variables(self):
        self.html_file_path = self.get_resource_path(r"presentation.html")
        self.mp3_file_path = self.get_resource_path(r"src\joyeux_noel.mp3")
        self.server_path = self.get_resource_path(self.mp3_file_path.replace("\\src\\joyeux_noel.mp3", "\\."))
        self.gpg_key_path = self.get_resource_path(r"src\key.asc")
        self.am_file_path = self.get_resource_path(r"src\am.png")
        self.im_file_path = self.get_resource_path(r"src\im.jpg")
        self.fav_file_path = self.get_resource_path(r"favicon.ico")
        self.server_result_queue = queue.Queue()

    def get_resource_path(self, relative_path) -> str:
        """Obtenir le chemin des ressources pour PyInstaller"""
        try:
            # PyInstaller crée un dossier temporaire et stocke les ressources dans _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def create_widgets(self):
        # Titre principal
        title_frame = tk.Frame(self.root, bg="#2c5530")
        title_frame.pack(pady=20)

        title_label = tk.Label(title_frame,
                               text="🎄 Joyeux Noël 🎄",
                               font=("Arial", 24, "bold"),
                               fg="#ffdd44",
                               bg="#2c5530")
        title_label.pack()

        subtitle_label = tk.Label(title_frame,
                                  text="Programme de déchiffrement et présentation",
                                  font=("Arial", 11),
                                  fg="#ffffff",
                                  bg="#2c5530")
        subtitle_label.pack()

        # Frame principal pour les boutons
        buttons_frame = tk.Frame(self.root, bg="#2c5530")
        buttons_frame.pack(expand=True, fill="both", padx=40, pady=20)

        # Style pour les boutons
        style = {
            'font': ('Arial', 11, 'bold'),
            'height': 2,
            'width': 35,
            'relief': 'raised',
            'bd': 3
        }

        # Bouton 1: Charger clé GPG
        btn_gpg = tk.Button(buttons_frame,
                            text="🔐 Charger une clé GPG privée",
                            bg="#cc3333",
                            fg="white",
                            activebackground="#aa2222",
                            command=self.load_gpg_key,
                            **style)
        btn_gpg.pack(pady=15)

        # Bouton 2: Déchiffrer et présenter
        btn_present = tk.Button(buttons_frame,
                                text="🎁 Déchiffrer et lancer présentation",
                                bg="#228844",
                                fg="white",
                                activebackground="#116622",
                                command=self.decrypt_and_present,
                                **style)
        btn_present.pack(pady=15)

        # Bouton 3: Lire musique
        btn_music = tk.Button(buttons_frame,
                              text="🎵 Lancer la musique de Noël",
                              bg="#4466cc",
                              fg="white",
                              activebackground="#2244aa",
                              command=self.toggle_music,
                              **style)
        btn_music.pack(pady=15)

        # Label de statut
        self.status_label = tk.Label(self.root,
                                     text="Prêt",
                                     font=("Arial", 10),
                                     fg="#ffffff",
                                     bg="#2c5530")
        self.status_label.pack(side="bottom", pady=10)

    def update_status(self, message):
        """Mettre à jour le message de statut"""
        self.status_label.config(text=message)
        self.root.update()

    def calculer_hash_fichier(self, chemin_fichier, algorithme='md5', taille_buffer=65536):
        """
        Calcule le hash d'un fichier en utilisant l'algorithme spécifié.

        Args:
            chemin_fichier (str): Chemin vers le fichier à hacher
            algorithme (str): Algorithme de hachage (md5, sha1, sha256, etc.)
            taille_buffer (int): Taille du buffer de lecture

        Returns:
            str: Le hash du fichier en format hexadécimal
        """

        hash_obj = hashlib.sha256()
        with open(chemin_fichier, 'rb') as f:
            for morceau in iter(lambda: f.read(4096), b""):
                hash_obj.update(morceau)
        return hash_obj.hexdigest()

    def auth_login(self, user_key, true_key):
        uk = self.calculer_hash_fichier(user_key, 'sha256')
        tk = self.calculer_hash_fichier(true_key, 'sha256')
        if uk == tk:
            return True
        else:
            return False

    def load_gpg_key(self):
        """Charger une clé GPG privée"""
        try:
            file_path = filedialog.askopenfilename(
                title="Sélectionner la clé GPG privée",
                filetypes=[("Fichiers ASC", "*.asc"), ("Tous les fichiers", "*.*")]
            )
            if file_path:
                self.update_status("Chargement de la clé GPG...")

                if self.auth_login(file_path, self.gpg_key_path):
                    import_result = str(1)
                    messagebox.showinfo("Succès",
                                        f"Clé GPG importée avec succès!\n"
                                        f"Nombre de clés: {import_result}")
                    self.update_status("Clé GPG chargée")
                else:
                    messagebox.showerror("Erreur", "Impossible d\'importer la clé GPG")
                    self.update_status("Erreur lors du chargement de la clé")

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du chargement de la clé GPG:\n{str(e)}")
            self.update_status("Erreur")

    def decrypt_and_present(self):
        """Déchiffrer le fichier HTML et lancer la présentation"""
        try:
            self.open_presentation()
            messagebox.showinfo("Succès", "Présentation déchiffrée et lancée!")
            self.update_status("Présentation en cours")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du déchiffrement:\n{str(e)}")
            self.update_status("Erreur")

    def toggle_music(self):
        """Lancer/arrêter la musique"""
        try:
            if not self.music_playing:
                self.play_music()
            else:
                self.stop_music()
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur avec la musique:\n{str(e)}")

    def play_music(self):
        """Lire le fichier MP3"""
        try:
            # Vérifier si le fichier MP3 existe
            if not os.path.exists(self.mp3_file_path):
                messagebox.showinfo("Information",
                                    "Fichier MP3 non trouvé. Veuillez placer \'joyeux_noel.mp3\' dans le dossier du programme.")
                return

            pygame.mixer.init()
            pygame.mixer.music.load(self.mp3_file_path)
            pygame.mixer.music.play(-1)  # Jouer en boucle

            self.music_playing = True
            self.update_status("🎵 Musique en cours...")

        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de lire la musique:\n{str(e)}")

    def stop_music(self):
        """Arrêter la musique"""
        try:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
            self.music_playing = False
            self.update_status("Musique arrêtée")
        except:
            pass

    def on_closing(self):
        """Gestionnaire de fermeture de l'application"""
        try:
            self.stop_music()
        except:
            pass
        self.root.destroy()

    def extract_text_from_html(self, html_content):
        """Extraire le texte du contenu HTML"""
        import re
        text = re.sub(r'<[^>]+>', '', html_content)
        return text

    def open_presentation(self, decrypted_content=None):
        """Ouvrir la présentation dans une fenêtre Tkinter au lieu d'un navigateur"""
        html_content = None
        try:
            if decrypted_content:
                # Utiliser le contenu déchiffré si fourni
                html_content = decrypted_content
            else:
                # Sinon, charger depuis le fichier
                with open(self.html_file_path, 'r', encoding='utf-8') as f:
                    html_content = f.read()

            # Afficher le contenu dans une fenêtre Tkinter
            self.display_content_in_tkinter(html_content)

            # Jouer la musique si nécessaire
            if not self.music_playing:
                self.play_music()

            self.update_status("Présentation ouverte avec succès")
        except Exception as e:
            self.update_status(f"Erreur lors de l'ouverture de la présentation: {e}")

    def display_image_in_tkinter(self, image_path, parent_widget):
        """Afficher une image dans un widget Tkinter"""
        try:
            # Ouvrir et redimensionner l'image
            img = Image.open(image_path)
            img = img.resize((400, 300), Image.LANCZOS)  # Ajuster selon vos besoins

            # Convertir en format Tkinter
            tk_img = ImageTk.PhotoImage(img)

            # Créer un label pour afficher l'image
            img_label = tk.Label(parent_widget, image=tk_img)
            img_label.image = tk_img  # Garder une référence pour éviter la suppression par le garbage collector
            img_label.pack(padx=10, pady=10)

            return img_label
        except Exception as e:
            print(f"Erreur lors de l'affichage de l'image: {e}")
            return None

    def display_content_in_tkinter(self, html_content):
        """Afficher le contenu du diaporama dans une fenêtre Tkinter"""
        import re

        # Créer une nouvelle fenêtre pour la présentation
        presentation_window = tk.Toplevel(self.root)
        presentation_window.title(" Joyeux Noël ! ")
        presentation_window.geometry("800x700")
        presentation_window.configure(background='white')
        presentation_window.config(cursor="heart")
        presentation_window.iconbitmap(self.fav_file_path)
        # Extraire les diapositives du HTML
        slides_content = re.findall(r'class: center, middle\s+(.+?)(?=---|\Z)', html_content, re.DOTALL)

        # Variables pour suivre la diapositive actuelle
        current_slide = tk.IntVar(value=0)

        # Fonction pour extraire le texte ou l'image d'une diapositive
        def parse_slide_content(slide_text):
            img_match = re.search(r'<img src="([^"]+)"', slide_text)
            if img_match:
                return {"type": "image", "src": img_match.group(1)}
            else:
                # Nettoyer le texte
                text = re.sub(r'#\s*', '', slide_text.strip())
                return {"type": "text", "content": text}

        # Analyser toutes les diapositives
        slides = [parse_slide_content(slide) for slide in slides_content]

        # Frame principale pour le contenu
        content_frame = tk.Frame(presentation_window, bg='white')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Label pour le texte ou l'image
        slide_content = tk.Label(content_frame, bg='white', font=('Helvetica', 36, 'bold'))
        slide_content.pack(fill=tk.BOTH, expand=True, pady=50)

        # Frame pour les boutons de navigation
        nav_frame = tk.Frame(presentation_window, bg='white')
        nav_frame.pack(fill=tk.X, padx=20, pady=20)

        # Dictionnaire pour stocker les images chargées
        image_cache = {}

        # Fonction pour afficher une diapositive
        def show_slide(index):
            # Vérifier les limites
            if index < 0:
                index = 0
            elif index >= len(slides):
                index = len(slides) - 1

            current_slide.set(index)
            slide = slides[index]

            # Effacer le contenu actuel
            slide_content.config(text="", image="")

            if slide["type"] == "text":
                # Afficher du texte
                slide_content.config(text=slide["content"],
                                     font=('Helvetica', 36, 'bold'),
                                     wraplength=700)
            else:
                # Afficher une image
                img_path = slide["src"].replace("/", os.path.sep)
                # Retirer le premier slash si présent
                if img_path.startswith(os.path.sep):
                    img_path = img_path[1:]

                # Chemin complet de l'image
                full_path = os.path.join(os.path.dirname(self.html_file_path), img_path)

                # Vérifier si l'image est déjà en cache
                if full_path not in image_cache:
                    try:
                        # Ouvrir et redimensionner l'image
                        img = Image.open(full_path)
                        img = img.resize((500, 500), Image.LANCZOS)

                        # Convertir en format Tkinter
                        tk_img = ImageTk.PhotoImage(img)
                        image_cache[full_path] = tk_img
                    except Exception as e:
                        print(f"Erreur lors du chargement de l'image {full_path}: {e}")
                        slide_content.config(text=f"[Erreur d'image: {e}]",
                                             font=('Helvetica', 18))
                        return

                # Afficher l'image depuis le cache
                slide_content.config(image=image_cache[full_path])

        # Fonction pour passer à la diapositive suivante
        def next_slide():
            show_slide(current_slide.get() + 1)

        # Fonction pour revenir à la diapositive précédente
        def prev_slide():
            show_slide(current_slide.get() - 1)

        # Boutons de navigation
        prev_button = tk.Button(nav_frame, text="◀", command=prev_slide,
                                font=('Helvetica', 24), bg='white',
                                width=5, height=1)
        prev_button.pack(side=tk.LEFT, padx=20)

        next_button = tk.Button(nav_frame, text="▶", command=next_slide,
                                font=('Helvetica', 24), bg='white',
                                width=5, height=1)
        next_button.pack(side=tk.RIGHT, padx=20)

        # Raccourcis clavier pour la navigation
        def key_handler(event):
            if event.keysym == 'Right':
                next_slide()
            elif event.keysym == 'Left':
                prev_slide()
            elif event.keysym == 'Escape':
                presentation_window.destroy()

        presentation_window.bind("<Key>", key_handler)

        # Afficher la première diapositive
        show_slide(0)


def main():
    """Fonction principale"""
    root = tk.Tk()
    app = JoyeuxNoelApp(root)

    # Gestionnaire de fermeture
    root.protocol("WM_DELETE_WINDOW", app.on_closing)

    root.mainloop()


if __name__ == "__main__":
    main()
