# Sistema de Repartiment de Menjar a Domicili 🍔🚴‍♂️

Aquest projecte és una aplicació web desenvolupada per gestionar comandes de menjar a domicili, des del registre de clients i restaurants fins a la gestió de comandes i repartiment. S'ha utilitzat el framework **Django** per a la seva implementació, integrant múltiples funcions per als diferents rols (clients, repartidors, restaurants i partners).

## Captures de Pantalla 📸

### Pantalla d'Inici de Sessió
![Pantalla d'Inici de Sessió](./images/inici_sessio.png)
La pantalla d'inici de sessió permet als usuaris accedir al sistema utilitzant les seves credencials.

### Pantalla de Registre de Partners
![Pantalla de Registre de Partners](./images/registre_partners.png)
El formulari de registre per als socis comercials (partners) està organitzat en un format "Linear Stepper", que guia l'usuari a través de seccions com Informació Personal, Informació de Contacte, Configuració del Compte i Informació del Negoci.

### Pantalla de Registre de Clients
![Pantalla de Registre de Clients](./images/registre_clients.png)
El formulari de registre per a clients segueix un format similar al dels partners i inclou informació personal, informació de contacte i adreça principal per a la recepció de comandes.

### Pantalla de Llistat de Restaurants
![Pantalla de Llistat de Restaurants](./images/llistat_restaurants.png)
Un cop registrat, el client pot veure els restaurants disponibles a la seva ciutat, ordenats pel millor puntuatge.

### Pantalla de Llistat de Plats
![Pantalla de Llistat de Plats](./images/llistat_plats.png)
Els clients poden seleccionar qualsevol plat del menú del restaurant triat i afegir-lo al carret de compra. És possible afegir plats de diferents restaurants al mateix carret.

### Funcions de Cerca i Filtres
![Funcions de Cerca i Filtres](./images/cerca_i_filtres.png)
El sistema permet ordenar els plats per preu, puntuació o tipus de menjar, a més de disposar d'una barra de cerca per trobar plats pel seu nom.

### Pantalla de Gestió del Carret de la Compra
![Gestió del Carret](./images/gestio_carret.png)
Els clients poden accedir al carret en qualsevol moment per revisar, afegir o eliminar plats, així com veure el cost total i les comissions de la plataforma.

### Pantalla del Procés de Comanda
![Procés de Comanda](./images/proces_comanda.png)
Un cop preparats per a fer la comanda, els clients poden confirmar la seva adreça de lliurament i introduir la informació de la targeta de crèdit.

### Pantalla de Gestió del Comanda (Client)
![Gestió de Comanda per al Client](./images/gestio_comanda_client.png)
Els clients poden veure l'estat del seu comanda, cancel·lar-lo o consultar els detalls del mateix.

### Pantalla de Gestió del Comanda (Restaurant)
![Gestió de Comanda per al Restaurant](./images/gestio_comanda_restaurant.png)
Els responsables de cuina poden gestionar les comandes, marcant quan estan en preparació o llestos per ser enviats.

### Pantalla de Gestió del Comanda (Repartidor)
![Gestió de Comanda per al Repartidor](./images/gestio_comanda_repartidor.png)
Els repartidors reben les comandes i poden veure la ubicació del lliurament a través del mapa. Un cop entregat, el repartidor pot marcar la comanda com a completada.

### Pantalla de Gestió de Restaurants per al Partner
![Gestió de Restaurants](./images/gestio_restaurants_partner.png)
Els partners poden gestionar els seus restaurants, afegint nous establiments o visualitzant les puntuacions i ressenyes dels clients.

### Pantalla de Gestió de Plats per al Partner
![Gestió de Plats](./images/gestio_plats_partner.png)
Els partners poden afegir o modificar els plats disponibles en el menú de cada restaurant.

### Pantalla de Gestió del Personal per al Partner
![Gestió de Personal](./images/gestio_personal_partner.png)
Els partners poden gestionar el personal, afegir repartidors i responsables de cuina, així com gestionar l'accés als comptes dels treballadors.

### Pantalla de Gestió de Ressenyes
![Gestió de Ressenyes](./images/gestio_ressenyes_partner.png)
Els partners poden veure les ressenyes dels clients, tant per a restaurants com per a plats específics, per tal de monitoritzar la satisfacció dels clients.

---
