#!/usr/bin/env python3
import urllib.request, json, ssl, tkinter as tk, os
from PIL import Image, ImageTk

# --- CONFIG ---
API_URL = "https://nary14.pythonanywhere.com"
HOSTNAME = "pc_sedape"
IMG_NAME = "vous avez été sédapé.jpg" # VERIFIE BIEN LE NOM ICI
# --------------

class SedapeLock:
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True)
        self.root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
        self.root.attributes('-topmost', True)
        self.root.bind("<Escape>", lambda e: self.quit_lock()) # Touche de secours

        # 1. Verification de l'image
        if not os.path.exists(IMG_NAME):
            print(f"!!! ERREUR : Le fichier {IMG_NAME} est introuvable dans ce dossier.")
            # On crée un fond rouge si l'image manque pour ne pas avoir de blanc
            self.root.configure(bg='red')
            tk.Label(root, text="ERREUR IMAGE MANQUANTE", fg="white", bg="red", font=("Arial", 30)).pack(expand=True)
        else:
            try:
                img = Image.open(IMG_NAME).resize((root.winfo_screenwidth(), root.winfo_screenheight()))
                self.photo = ImageTk.PhotoImage(img)
                tk.Label(root, image=self.photo, borderwidth=0).pack()
            except Exception as e:
                print(f"Erreur ouverture image: {e}")

        print("Lancement de la surveillance...")
        self.check_loop()

    def check_loop(self):
        try:
            ctx = ssl._create_unverified_context()
            url = f"{API_URL}/status/{HOSTNAME}"
            with urllib.request.urlopen(url, context=ctx, timeout=3) as r:
                res = json.loads(r.read().decode())
                print(f"Serveur dit : {res['unlocked']}") # Affiche False ou True dans le terminal
                if res['unlocked'] == True:
                    print("DÉVERROUILLAGE !")
                    self.quit_lock()
                    return
        except Exception as e:
            print(f"Erreur réseau : {e}")
        
        self.root.after(2000, self.check_loop)

    def quit_lock(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    SedapeLock(root)
    root.mainloop()
