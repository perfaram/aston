from tkinter.simpledialog import Dialog
from tkinter import Label, Entry, messagebox
from tkinter import LEFT, W, E
from OTPControllers import Controller


class NewAccountDialog(Dialog):
    def __init__(self, controller: Controller, parent = None):
        self.controller = controller
        Dialog.__init__(self, parent, "Nouveau compte")

    def destroy(self):
        self.site_entry = None
        self.username_entry = None
        Dialog.destroy(self)

    def body(self, master):
        w = Label(master, text="Site", justify=LEFT)
        w.grid(row=0, padx=5, sticky=W)
        self.site_entry = Entry(master, name="site_entry")
        self.site_entry.grid(row=1, padx=5, sticky=W+E)

        w = Label(master, text="Username", justify=LEFT)
        w.grid(row=2, padx=5, sticky=W)
        self.username_entry = Entry(master, name="username_entry")
        self.username_entry.grid(row=3, padx=5, sticky=W+E)

        w = Label(master, text="Key", justify=LEFT)
        w.grid(row=4, padx=5, sticky=W)
        self.secret_key_entry = Entry(master, name="secret_key_entry")
        self.secret_key_entry.grid(row=5, padx=5, sticky=W+E)

        return self.site_entry

    def validate(self):
        # pour respecter le pattern MVC, la vue (cette classe) appelle le contrôleur quand l'user clic sur OK (`intent_new_acccount`)
        # Charge alors au contrôleur de valider et soit raise une erreur si la validation échoue (ici, ValueError si une clef n'est pas en Base32 valide)
        # soit enregistrer le nouveau compte.
        # Et, charge alors à la vue d'afficher l'erreur et de permettre à l'user de corriger, ou si le contrôleur n'a pas raise, de se fermer. 
        result = self.get_result()
        try:
            self.controller.intent_new_account(result)
        except ValueError:
            messagebox.showwarning(
                "Valeur interdite",
                "Veuillez remplir les valeurs et réessayer.",
                parent = self
            )
            return False
        except:
            messagebox.showwarning(
                "Une erreur est survenue",
                "Impossible de créer un compte.",
                parent = self
            )
            return False

        return True

    def get_result(self):
        site_value = self.site_entry.get()
        username_value = self.username_entry.get()
        secret_key_value = self.secret_key_entry.get()

        if not site_value or not username_value or not secret_key_value:
            raise ValueError() # il faut que l'utilisateur remplisse les cases

        return {
            "site": site_value,
            "username": username_value,
            "secret_key": secret_key_value,
        }
