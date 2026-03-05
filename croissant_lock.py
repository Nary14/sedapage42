#!/usr/bin/env python3
#!/usr/bin/env python3
import urllib.request, json, ssl, tkinter as tk, os
from PIL import Image, ImageTk

# --- CONFIGURATION ---
API_URL = "https://nary14.pythonanywhere.com"
HOSTNAME = "pc_sedape"
IMG_NAME = "sedape.jpg" 
# ---------------------

class SedapeLock:
    def __init__(self, root):
        self.root = root
        
        # 1. Setup plein écran total
        self.root.overrideredirect(True)
        self.root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
        self.root.attributes('-topmost', True)
        self.root.config(cursor="none")
        self.root.configure(bg='black')

        # 2. TOUCHE DE SECOURS PERSONNALISÉE : Ctrl + Alt + Tab + F8
        # Note : On bind sur le root pour capturer partout
        self.root.bind("<Control-Alt-F8>", lambda e: self.quit_lock())
        
        # Optionnel : On garde Echap pour tes tests rapides (tu peux supprimer la ligne après)
        self.root.bind("<Escape>", lambda e: self.quit_lock())

        # 3. Chargement de l'image
        if not os.path.exists(IMG_NAME):
            self.root.configure(bg='red')
            tk.Label(root, text=f"ERREUR: {IMG_NAME} non trouvé", fg="white", bg="red", font=("Arial", 25)).pack(expand=True)
        else:
            try:
                img = Image.open(IMG_NAME).resize((root.winfo_screenwidth(), root.winfo_screenheight()))
                self.photo = ImageTk.PhotoImage(img)
                tk.Label(root, image=self.photo, borderwidth=0).pack()
            except Exception as e:
                print(f"Erreur image: {e}")

        # 4. CAPTURE DU CLAVIER (Anti-Touche Windows / Alt-Tab)
        # On attend 100ms que la fenêtre soit bien lancée avant de "grab"
        self.root.after(100, self.force_focus)

        print(f"[*] Surveillance lancée. Secours : Ctrl+Alt+Tab+F8")
        self.check_loop()

    def force_focus(self):
        """Force la fenêtre à capturer toutes les entrées du système"""
        self.root.focus_force()
        self.root.grab_set_global() # Bloque les touches Windows/Alt-Tab sur Linux

    def check_loop(self):
        try:
            ctx = ssl._create_unverified_context()
            url = f"{API_URL}/status/{HOSTNAME}"
            
            with urllib.request.urlopen(url, context=ctx, timeout=3) as r:
                res = json.loads(r.read().decode())
                
                if res.get('unlocked') == True:
                    print("[!] Signal reçu !")
                    # Reset Serveur
                    try:
                        urllib.request.urlopen(f"{API_URL}/reset/{HOSTNAME}", context=ctx)
                    except:
                        pass
                    self.quit_lock()
                    return
        except Exception as e:
            print(f"Erreur réseau : {e}")
        
        # Sécurité : On s'assure qu'on a toujours le focus
        self.root.after(2000, self.check_loop)

    def quit_lock(self):
        print("[*] Fermeture du lock...")
        self.root.grab_release() # Libère le clavier
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SedapeLock(root)
    root.mainloop()
