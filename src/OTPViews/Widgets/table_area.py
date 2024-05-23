from tkinter import ttk, Menu, Event
from tkinter import W as WEST
from tkinter.messagebox import askyesno
from AppStorage import Models
from OTPControllers import Controller
from .historique_window import Historique


class TableArea(ttk.Frame):
    def __init__(self, container: ttk.Frame, controller: Controller):
        super().__init__(container)
        self.controller = controller

        self.counters = {}

        self.canvas_area = ttk.Frame(self, width=500, height=400)
        self.canvas_area.pack()
        self.table()

    def table(self):
        self.tree = ttk.Treeview(self.canvas_area, height=10, columns=(1, 2))
        self.tree.grid(row=5, column=0, columnspan=3)
        self.tree.heading("#0", text="Site", anchor=WEST)
        self.tree.heading("#1", text="Username", anchor=WEST)
        self.tree.heading("#2", text="Code", anchor=WEST)
        self.tree.bind("<Double-1>", self.on_double_click) # bind à l'event "double clic"
        self.tree.bind("<Button-3>", self.on_right_click) # bind à l'event "clic droit"

        self.controller.register_for_model_updates(Models.Account, self)

    def reload(self):
        new_records = self.controller.get_all_accounts()
        new_records_ids = [a.id for a in new_records]
        prev_record_ids = [int(iid) for iid in self.tree.get_children()]
        
        deleted = [iid for iid in prev_record_ids if iid not in new_records_ids]
        for iid in deleted:
            self.tree.delete(iid)
            if iid in self.counters:
                del self.counters[iid]
        
        for account in new_records:
            if account.id in prev_record_ids: # un counter peut être en cours, le préserver
                otp_field = self.tree.item(account.id)["values"][1]
                self.tree.item(account.id, text=account.site, values=(account.username, otp_field))
                continue
            self.tree.insert("", 0, iid= account.id, text=account.site, values=(account.username, "*** ***"))


    def get_table_selected_item_id(self) -> int:
        sel = self.tree.selection()
        if not sel:
            return None
        iid = int(sel[0])
        return iid

    def on_double_click(self, event: Event):
        account_id = self.get_table_selected_item_id()
        if not account_id:
            return

        if account_id in self.counters:
            return # déjà visible

        account = self.controller.get_account(account_id)
        totp_code = self.controller.intent_generate_totp(account_id)
        self.counters[account_id] = 30
        
        def counter_callback():
            if account_id not in self.counters:
                # timer supprimé (peut arriver si l'user a supprimé le compte)
                return
            if self.counters[account_id] == 0:
                del self.counters[account_id]
                self.tree.item(account_id, text=account.site, values=(account.username, "*** ***"))
                return

            displayed_value = totp_code + " [" + str(self.counters[account_id]) + "s]"
            self.tree.item(account_id, text=account.site, values=(account.username, displayed_value))
            self.counters[account_id] = self.counters[account_id] - 1
            self.after(1000, counter_callback) # start the update 1 second later

        counter_callback()


    def on_right_click(self, event: Event):
        if not self.tree.selection():
            return
        m = Menu(self, tearoff = 0) 
        m.add_command(label ="Supprimer", command=self.on_delete_clicked)
        m.add_command(label="Historique", command=self.on_historique_clicked)

        # explicitement faire appeler ce callback quand le menu du clic-droit perd le focus
        # (=quand l'user interagit ailleurs, clic en-dehors par exemple)
        # est requis sur certains systèmes, sinon le menu reste là 
        def on_close(event: Event):
            m.destroy()
        m.bind("<FocusOut>", on_close)

        try: 
            m.tk_popup(event.x_root, event.y_root)
        finally: 
            m.grab_release() 

    def on_delete_clicked(self):
        account_id = self.get_table_selected_item_id()
        account = self.controller.get_account(account_id)
        user_is_sure = askyesno(f"Suppression de {account.site}:{account.username}", "Êtes-vous certain de vouloir supprimer ce compte?")
        if not user_is_sure:
            return
   
        
        self.controller.intent_delete_account(account_id)
        # pas besoin de reload, car le contrôleur me reloadera
        
    def on_historique_clicked(self):
        account_id = self.get_table_selected_item_id()
        account = self.controller.get_account(account_id)
        historique_window = Historique()
        historique = account.liste_historique()
        historique_window.show_historique(historique)
				
		