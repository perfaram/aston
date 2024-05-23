from sqlalchemy import Column, Integer, String, ForeignKey
from ..Database import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship
from sqlalchemy import delete, select


class Account(BaseModel):
    '''
    Chaque instance (dans la base de donnée, enregistrement) de ce modèle représente un compte de l'utilisateur ayant la 2FA activée,
    et pour lequel l'utilisateur souhaite utiliser notre application pour générer les codes TOTP. 
    '''
    
    __tablename__ = 'accounts' # le nom de la table SQL contenant les comptes, générée par SQLAlchemy selon le schéma défini ci-dessous. 
    

    # MARK - Schéma SQL

    id: Mapped[int] = mapped_column(primary_key=True)
    
    site = Column(String)
    username = Column(String)
    secret_key = Column(String)

    generations: Mapped[list["Generation"]] = relationship(back_populates="account") # ceci va générer une foreign key constraint. 


    # MARK - Méthodes boilerplate. 

    def __init__(self, site: str, username: str, secret_key: str):
        super(BaseModel,self).__init__()

        self.site = site
        self.username = username
        self.secret_key = secret_key

    def __repr__(self) -> str:
        return "<Account(site='%s', username='%s')>" % (self.site, self.username)

    @staticmethod
    def get_all(db_session) -> list['Account']:
        stmt = select(Account)
        results = db_session.execute(stmt)
        return results.scalars()

    @staticmethod
    def get_by_id(db_session, account_id: int) -> 'Account':
        stmt = select(Account).filter_by(id=account_id)
        result = db_session.execute(stmt).fetchone()[0]
        return result

    @staticmethod
    def upsert(db_session, account: 'Account'):
        """Insère ou modifie un enregistrement."""
        db_session.merge(account)
        db_session.commit()

    @staticmethod
    def delete(db_session, account_id: int) -> int:
        """Supprime l'entrée portant l'identifiant `account_id`. 
        Retourne le nombre d'entrées supprimées (l'id étant unique, devrait tjrs être 1).
        """
        stmt = delete(Account).where(Account.id == account_id)
        result = db_session.execute(stmt)
        db_session.commit()
        return result.rowcount
        
    def liste_historique(self):
        return self.generations