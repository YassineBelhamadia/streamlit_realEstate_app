from models import Ville, Equipement, Annonce, AnnonceEquipement
from sqlalchemy.sql import func
import pandas as pd
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts import get_session


def get_annonces_by_ville(ville_name):
    """Fetch annonces based on the ville name."""
    session = get_session()
    results = session.query(Annonce).join(Ville).filter(Ville.nom == ville_name).all()
    session.close()
    # Make sure to convert each annonce to a dictionary or return relevant fields
    return pd.DataFrame([annonce.to_dict() for annonce in results])


def get_annonces_by_price_range(min_price, max_price):
    """Fetch annonces by price range."""
    session = get_session()
    results = session.query(Annonce).filter(Annonce.prix >= min_price, Annonce.prix <= max_price).all()
    session.close()
    # Ensure `to_dict` is implemented or return fields directly
    return pd.DataFrame([annonce.to_dict() for annonce in results])


def get_annonces_filtered(min_price, max_price, min_rooms, max_rooms, min_baths, max_baths, ville_names, equipment_ids, start_date, end_date):
    """
    Fetch annonces based on multiple filters and return dictionaries.
    """
    session = get_session()
    query = session.query(Annonce).join(Ville).join(AnnonceEquipement, isouter=True)

    # Apply filters
    query = query.filter(
        Annonce.prix.between(min_price, max_price),
        Annonce.nb_pieces.between(min_rooms, max_rooms),
        Annonce.nb_salles_bain.between(min_baths, max_baths),
        Annonce.date_publication.between(start_date, end_date),
    )

    if ville_names:
        query = query.filter(Ville.nom.in_(ville_names))

    if equipment_ids:
        query = query.filter(AnnonceEquipement.equipement_id.in_(equipment_ids))

    # Fetch results directly into a list of dictionaries
    results = [{
        'Listing title': annonce.titre,
        'number of bedrooms': annonce.nb_pieces,
        'number of bathrooms': annonce.nb_salles_bain,
        'surface area M3' : annonce.surface,
        'price (MAD)': annonce.prix,
        'Date of pub': annonce.date_publication,
        'city': annonce.ville.nom  # Add fields as necessary
    } for annonce in query.distinct().all()]
    
    session.close()
    return results


def get_annonces_count_by_ville():
    """Fetch the number of annonces per ville."""
    session = get_session()
    results = session.query(Ville.nom, func.count(Annonce.id)).join(Annonce).group_by(Ville.nom).order_by(func.count(Annonce.id).desc()).limit(10).all()
    session.close()
    return pd.DataFrame(results, columns=["City", "Count"])


def get_price_distribution():
    """Fetch data for a histogram of price distribution."""
    session = get_session()
    results = session.query(Annonce.prix).all()
    session.close()
    return pd.DataFrame(results, columns=["Price"])


def get_price_boxplot_by_ville():
    """Fetch data for a boxplot of price ranges by ville."""
    session = get_session()
    results = session.query(Ville.nom, Annonce.prix).join(Ville).all()
    session.close()
    return pd.DataFrame(results, columns=["City", "Price"])


def get_equipment_distribution():
    """Fetch the percentage of annonces with specific equipment."""
    session = get_session()
    results = session.query(Equipement.nom, func.count(AnnonceEquipement.annonce_id)).join(AnnonceEquipement).group_by(Equipement.nom).all()
    session.close()
    return pd.DataFrame(results, columns=["Equipment", "Count"])


def get_average_rooms_and_baths_by_ville():
    """Fetch the average number of rooms and baths per ville."""
    session = get_session()
    results = session.query(
        Ville.nom,
        func.avg(Annonce.nb_pieces).label("Average_Rooms"),
        func.avg(Annonce.nb_salles_bain).label("Average_Baths")
    ).join(Ville).group_by(Ville.nom).limit(15).all()
    session.close()
    return pd.DataFrame(results, columns=["City", "Average_Rooms", "Average_Baths"])


def get_annonces_over_time():
    """Fetch data for the temporal evolution of annonces."""
    session = get_session()
    results = session.query(
        func.date_trunc('month', Annonce.date_publication).label('Month'),
        func.count(Annonce.id).label('Count')
    ).group_by('Month').order_by('Month').all()
    session.close()
    return pd.DataFrame(results, columns=["Month", "Count"])


def get_all_cities():
    """Fetch all unique city names from the Ville table."""
    session = get_session()
    cities = session.query(Ville.nom).distinct().all()
    session.close()
    return pd.DataFrame(cities, columns=["City"])


def get_all_equipments():
    """Fetch all unique equipment names from the Equipement table."""
    session = get_session()
    equipments = session.query(Equipement.nom).distinct().all()
    session.close()
    return pd.DataFrame(equipments, columns=["Equipment"])
