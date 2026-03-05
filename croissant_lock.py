#!/usr/bin/env python3
import urllib.request, json, ssl, tkinter as tk, os
from PIL import Image, ImageTk

# --- CONFIGURATION ---
API_URL = "https://nary14.pythonanywhere.com"
HOSTNAME = "pc_sedape"
IMG_NAME = "sedape.jpg" 

class SedapeLock:
    def __init__(self, root):
        self.root = root
        
        # Compteur pour la touche de secours
        self.f8_count = 0
        
        # Setup plein écran
        self.root.overrideredirect(True)
        self.root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
        self.root.attributes('-topmost', True)
        self.root.config(cursor="none")
        self.root.configure(bg='black')

        # Liaison de la touche F8 à notre fonction de comptage
        self.root.bind("<KeyRelease-F8>", self.secret_emergency_exit)
        
        # Chargement de l'image
        if not os.path.exists(IMG_NAME):
            self.root.configure(bg='red')
            tk.Label(root, text="IMAGE MANQUANTE", fg="white", bg="red", font=("Arial", 25)).pack(expand=True)
        else:
            try:
                img = Image.open(IMG_NAME).resize((root.winfo_screenwidth(), root.winfo_screenheight()))
                self.photo = ImageTk.PhotoImage(img)
                tk.Label(root, image=self.photo, borderwidth=0).pack()
            except Exception as e:
                print(f"Erreur image: {e}")

        # CAPTURE TOTALE DU CLAVIER (Anti-Windows, Alt-Tab, etc.)
        self.root.after(100, self.start_grabbing)
        
        print(f"[*] Lock actif. Appuyez 10 fois sur F8 pour forcer la sortie.")
        self.check_loop()

    def start_grabbing(self):
        """Prend le contrôle exclusif du clavier et de la souris"""
        self.root.focus_force()
        self.root.grab_set_global()

    def secret_emergency_exit(self, event):
        """Incrémente le compteur à chaque appui sur F8"""
        self.f8_count += 1
        print(f"F8 pressé ({self.f8_count}/10)")
        
        if self.f8_count >= 10:
            print("[!] Code de secours activé !")
            self.quit_lock()

    def check_loop(self):
        try:
            ctx = ssl._create_unverified_context()
            url = f"{API_URL}/status/{HOSTNAME}"
            with urllib.request.urlopen(url, context=ctx, timeout=3) as r:
                res = json.loads(r.read().decode())
                if res.get('unlocked') == True:
                    # Reset automatique sur le serveur
                    try:
                        urllib.request.urlopen(f"{API_URL}/reset/{HOSTNAME}", context=ctx)
                    except:
                        pass
                    self.quit_lock()
                    return
        except:
            pass
        
        # Si on a perdu le "grab" (parfois Ubuntu essaie de le reprendre)
        # on le redemande discrètement
        self.root.grab_set_global()
        self.root.after(2000, self.check_loop)

    def quit_lock(self):
        print("[*] Libération du système...")
        self.root.grab_release()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SedapeLock(root)
    root.mainloop()
