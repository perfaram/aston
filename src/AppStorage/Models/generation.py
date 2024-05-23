from typing import List
import datetime
from sqlalchemy import Column, Integer, String,DATETIME, ForeignKey
from ..Database import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship
from .account import Account

class Generation(BaseModel):
    '''
    Record for a use of an account (i.e., the OTP code was generated). 
    Used to keep history.
    '''
    __tablename__ = 'generations'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id", ondelete='CASCADE'))
    account: Mapped["Account"] = relationship(back_populates="generations")

    timestamp = Column(DATETIME)

    def __init__(self, account: Account):
        super(BaseModel,self).__init__()
        
        #self.account = account
        self.timestamp = datetime.datetime.now()
        account.generations.append(self)

    def __repr__(self):
        return "<Generation(account='%s', timestamp='%s')>" % (self.account, self.timestamp)

    @staticmethod
    def upsert(db_session, account: 'Account'):
        """Insère ou modifie un enregistrement."""
        db_session.merge(account)
        db_session.commit()
