from tkinter import filedialog
from AppStorage import OTPDatabase, Models, BaseModel
import pyotp
from base64 import b32decode
from binascii import Error as Base32DecodingError


class Controller:
    '''
    Cette app, qui utilise le pattern MVC, est assez simple et ne contient qu'un unique contrôleur, cette classe `Controller`. 
    Il est en charge 
    - d'obtenir les données depuis de la base de données et de les transmettre aux Views, ainsi que 
    - de générer les codes OTPs, et 
    - valider les nouveaux comptes 2FA avant de les enregistrer. 
    '''

    def __init__(self, view, database: OTPDatabase):
        self.view = view
        self.database = database
        self.registered_for_model_updates = {}

    def run(self):
        '''
        Configure la view principale de ce contrôleur (la MainWindow) et lance la boucle principale de tkinter. 
        '''
        self.view.setup(self)
        self.view.loop()


    # MARK - Méthodes générales pour la cohérence vue-modèle

    def register_for_model_updates(self, model: BaseModel, target):
        """
        Cette méthode permet à une classe de s'inscrire pour être notifiée des changements concernant un modèle
        (par exemple ajout d'un nouvel enregistrement de ce modèle dans la base de données - ici typiquement un nouveau compte). 
        Il s'agit d'une implémentation relativement "bare-bones", simpliste et peu granulaire, du pattern "observer", qu'on peut 
        remarquer en Java, ou bien sous le nom de "key-value observing", en Objective-C et en Swift. 
        """
        if model.__name__ not in self.registered_for_model_updates:
            self.registered_for_model_updates[model.__name__] = []

        self.registered_for_model_updates[model.__name__].append(target)
        target.reload() # notifier une première fois, pour informer des données initiales. 

    def trigger_updates_for_model(self, model: BaseModel):
        """
        Cette méthode, qui ne vise qu'à être utilisée par Controller, permet de notifier les classes qui se sont préalablement
        inscrites, concernant un modèle spécifique, via la méthode `register_for_model_updates`. 
        """
        for target in self.registered_for_model_updates[model.__name__]:
            target.reload()


    # MARK - Opérations de gestion sur les comptes 2FA (lister, créer, supprimer)

    def get_all_accounts(self) -> list[Models.Account]:
        return Models.Account.get_all(self.database.session).all()

    def get_account(self, id: int):
        return Models.Account.get_by_id(self.database.session, id)

    def validate_new_account(self, account_dict):
        try:
            key = account_dict["secret_key"].strip()
            b32decode(key, casefold=True)
        except Base32DecodingError:
            raise ValueError() # on isole la vue de détails d'implémentation, comme le type de l'erreur
            # et on construit entre la vue et le contrôleur un contrat direct

    def create_new_account(self, account_dict):
        new_object = Models.Account(account_dict["site"], account_dict["username"], account_dict["secret_key"])
        Models.Account.upsert(self.database.session, new_object)
        self.trigger_updates_for_model(Models.Account)

    def intent_delete_account(self, id):
        Models.Account.delete(self.database.session, id)
        self.trigger_updates_for_model(Models.Account)

    def intent_new_account(self, account_dict):
        """
        Gère et exécute l'intention de l'utilisateur de créer un nouveau compte. 

        La vue indique cette intention en appelant cette méthode, mais c'est au contrôleur de valider les données 
        indiquées par celui-ci, et de les stocker ensuite. 
        Cette méthode laisse les erreurs raised par les deux qu'elle appelle "bubble up" à son propre appelant, la vue. 
        """
        self.validate_new_account(account_dict)
        self.create_new_account(account_dict)


    # MARK - Opérations applicatives sur les comptes 2FA (générer un code)

    def intent_generate_totp(self, account_id: int) -> str:
        """
        Génère un code TOTP valide maintenant. 
        """
        account = self.get_account(account_id)
        totp = pyotp.TOTP(account.secret_key)
        now = totp.now()

        new_gen = Models.Generation(account)
        Models.Account.upsert(self.database.session, account)

        return now