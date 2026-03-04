#!/usr/bin/env python3
import tkinter as tk
from PIL import Image, ImageTk
import urllib.request
import json
import ssl

# --- CONFIGURATION ---
IMAGE_FILE = "vous avez été sédapé.jpg"
API_URL = "https://nary14.pythonanywhere.com"
HOSTNAME = "pc_sedape" 
# ---------------------

class SedapeLock:
    def __init__(self, root):
        self.root = root
        
        # 1. Configuration plein écran
        self.root.overrideredirect(True) 
        self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}+0+0")
        self.root.attributes('-topmost', True)
        self.root.config(cursor="none")
        self.root.configure(background='black')

        # TOUCHE D'URGENCE : Appuie sur Echap pour quitter direct pendant tes tests
        self.root.bind("<Escape>", lambda e: self.quit_lock())

        # 2. Chargement de l'image
        try:
            img = Image.open(IMAGE_FILE)
            img = img.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()), Image.Resampling.LANCZOS)
            self.photo = ImageTk.PhotoImage(img)
            self.label = tk.Label(root, image=self.photo, borderwidth=0)
            self.label.pack(expand=True, fill="both")
        except Exception as e:
            print(f"Erreur image : {e}")

        # 3. Blocage total
        self.root.after(100, self.start_grab)
        self.root.bind("<FocusOut>", lambda e: self.root.focus_force())

        # 4. Lancement de la vérification à distance
        self.root.after(1000, self.check_remote_unlock)

    def start_grab(self):
        self.root.grab_set_global()
        self.root.focus_force()

    def check_remote_unlock(self):
        try:
            url = f"{API_URL}/status/{HOSTNAME}"
            
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            
            req = urllib.request.Request(url)
            # J'ai augmenté le timeout à 5 secondes ici :
            with urllib.request.urlopen(req, context=ctx, timeout=5) as response:
                data = json.loads(response.read().decode())
                
                if data.get("unlocked") == True:
                    print("Signal de déverrouillage reçu !")
                    self.quit_lock()
                    return 
        except Exception as e:
            # Maintenant on affiche l'erreur dans le terminal
            print(f"Erreur de communication avec le serveur : {e}")
        
        # On relance la vérification dans 2 secondes
        self.root.after(2000, self.check_remote_unlock)

    def quit_lock(self):
        self.root.grab_release()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SedapeLock(root)
    root.mainloop()
