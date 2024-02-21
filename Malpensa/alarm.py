import os
import tkinter as tk
from tkinter import messagebox

class FileScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ALARM")
        self.bg_original_color = self.root.cget('bg')

        # Nom du fichier à vérifier
        self.file_name = 'alarm.txt'

        # Label pour afficher l'état du fichier
        self.status_label = tk.Label(root, text="No internal disruption predicted")
        self.status_label.pack(pady=20)

        # Bouton pour quitter l'application
        quit_button = tk.Button(root, text="Quit", command=root.destroy)
        quit_button.pack()

        # Vérifier le fichier toutes les 2 secondes (ajustable selon vos besoins)
        self.check_file()

    def color_bg_in_red(self):
        self.root.configure(bg='red')
        if os.path.exists(self.file_name):
            self.root.after(500, self.color_bg_in_original_color)
        else:
            self.root.after(500, self.check_file)

    def color_bg_in_original_color(self):
        self.root.configure(bg=self.bg_original_color)
        if os.path.exists(self.file_name):
            self.root.after(500, self.color_bg_in_red)
        else:
            self.root.after(500, self.check_file)


    def check_file(self):
        if os.path.exists(self.file_name):
            time = "12pm15"
            area = "check-in"
            number_of_passenger = "2"
            max_time = "40"
            # Fichier détecté, mettre à jour le label
            self.status_label.config(text=f'Disruption predicted for {time} at area {area} for {number_of_passenger} (waited for more than {max_time})')

            
            # Changer temporairement la couleur de fond de la fenêtre en rouge
            self.color_bg_in_red()

        else:
            # Fichier non détecté, mettre à jour le label
            self.status_label.config(text='No internal disruption predicted')

        # Réexécuter la vérification après 2 secondes
        self.root.after(800, self.check_file)

if __name__ == "__main__":
    root = tk.Tk()
    app = FileScannerApp(root)
    root.geometry("800x500")
    root.mainloop()
