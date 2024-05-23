from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from .base_model import BaseModel
from ..configuration import Configuration


class OTPDatabase:
    '''
    Objet configurant et contenant la connection à la base de données (ici une SQLite locale). 
    '''

    def __init__(self) -> None:
        self.Engine = create_engine(Configuration.get_instance().database_path)
        self.BASE = BaseModel
        self.BASE.metadata.create_all(self.Engine)

        self.session_factory = sessionmaker(bind=self.Engine)
        self.session = self.session_factory()
