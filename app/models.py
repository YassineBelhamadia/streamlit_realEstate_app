# app/models.py

from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Ville(Base):
    __tablename__ = 'ville'
    id = Column(Integer, primary_key=True)
    nom = Column(String)
    
    def to_dict(self):
        return {
            "id": self.id,
            "nom": self.nom,
        }

class Equipement(Base):
    __tablename__ = 'equipement'
    id = Column(Integer, primary_key=True)
    nom = Column(String)

    def to_dict(self):
        return {
            "id": self.id,
            "nom": self.nom,
        }

class Annonce(Base):
    __tablename__ = 'annonce'
    id = Column(Integer, primary_key=True)
    titre = Column(String)
    prix = Column(Float)
    surface = Column(Float)
    date_publication = Column(Date)
    nb_pieces = Column(Integer)
    nb_salles_bain = Column(Integer)
    ville_id = Column(Integer, ForeignKey('ville.id'))
    ville = relationship('Ville')

    équipements = relationship('Equipement', secondary='annonce_equipement')

    def to_dict(self):
        return {
            "id": self.id,
            "prix": self.prix,
            "surface": self.surface,
            "nb_pieces": self.nb_pieces,
            "nb_salles_bain": self.nb_salles_bain,
            "date_publication": self.date_publication,
            "ville": self.ville.nom,  # Assuming a relationship with Ville
        }

class AnnonceEquipement(Base):
    __tablename__ = 'annonce_equipement'
    annonce_id = Column(Integer, ForeignKey('annonce.id'), primary_key=True)
    equipement_id = Column(Integer, ForeignKey('equipement.id'), primary_key=True)

    def to_dict(self):
        return {
            "annonce_id": self.annonce_id,
            "equipement_id": self.equipement_id,
        }
