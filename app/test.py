# testing how the queries work
from queries import (
    get_annonces_by_ville,
    get_annonces_filtered,
    get_annonces_count_by_ville,
    get_price_distribution,
    get_price_boxplot_by_ville,
    get_equipment_distribution,
    get_average_rooms_and_baths_by_ville,
    get_annonces_over_time,
    get_all_cities,
    get_all_equipments,
    get_equipement_ids_by_names
)

print(get_equipement_ids_by_names(['Ascenseur','Parking']))

