import mysql.connector
from os import listdir as OS_listdir
from os import walk
from os import path as OS_path
import os
from copy import deepcopy
from mutagen.flac import FLAC as mutagen_FLAC
from mutagen.easyid3 import EasyID3 as mutagen_EasyID3



def recuperer_infos_musique_mp3(tags):
    titre = str()
    artiste = str()
    genre = str()
    album = str()
    # on recupere les donnees dans chaque variable correspondante
    for key in tags.keys():
        if key == "title":
            titre = tags[key][0]
        elif key == "artist":
            artiste = tags[key][0]
        elif key == "genre":
            genre = tags[key][0]
        elif key == "album":
            album = tags[key][0]
    # on regarde si des variables sont vides et on les remplis manuellement
    if titre == str():
        titre = "unknown"
    if artiste == str():
        artiste = "unknown"
    if genre == str():
        genre = "unknown"
    if album == str():
        album = "unknown"
    
    return titre, artiste, genre, album

def il_manque_une_info(genre, artiste):
    if genre == "Genre inconnu" or artiste == "Interprète inconnu":
        return True
    return False

def est_dans_bdd_erreurs(path, cursor):
    sql = "SELECT * FROM problemes WHERE path = %s"
    cursor.execute(sql, (path,))
    result = cursor.fetchall()
    if len(result) == 0:
        return False
    return True

def est_dans_bdd_wav(path, cursor):
    sql = "SELECT * FROM wav WHERE path = %s"
    cursor.execute(sql, (path,))
    result = cursor.fetchall()
    if len(result) == 0:
        return False
    return True

#id 	titre 	artiste 	genre 	album 	source 	path 	utilisateur 

#----------------------------------------------------------------------------------------------------
#                                       actions pour la bdd
#----------------------------------------------------------------------------------------------------
def bdd_connexion(host_, database_, user_, password_):
    connection = mysql.connector.connect(host=host_, database=database_, user=user_, password=password_)
    if connection.is_connected():
        return connection
    print("Erreur lors de la tentative de connexion...")
    return False

def est_dans_bdd(lien_fichier, cursor):
    sql = "SELECT * FROM musiques WHERE path = %s" # verifier le nom des champs...
    cursor.execute(sql, (lien_fichier,))
    result = cursor.fetchall()
    if len(result) == 0:
        return False
    return True

def ajouter_dans_bdd(titre, artiste, genre, album, source, chemin, statut, cursor, connexion):
    if not le_genre_existe_deja(genre, cursor):
        ajout_du_genre(genre, cursor, connexion)

    genre = recuperation_id_genre(genre, cursor)
    source = recuperation_id_source(source, cursor)
    statut = recuperation_id_utilisateur(statut, cursor)
    cursor.execute("INSERT INTO musiques (titre, artiste, genre, album, source, path, utilisateur) VALUES (%s,%s,%s,%s,%s,%s,%s)", (titre, artiste, genre, album,source, chemin, statut))
    connexion.commit()

def ajouter_dans_bdd_des_erreurs(titre, artiste, genre, album, source, chemin, statut, cursor, connexion):
        statut = recuperation_id_utilisateur(statut, cursor)
        cursor.execute("INSERT INTO problemes (titre, artiste, genre, album, source, path, utilisateur) VALUES (%s,%s,%s,%s,%s,%s,%s)", (titre, artiste, genre, album,source, chemin, statut))
        connexion.commit()

def ajouter_dans_bdd_des_wav(titre, artiste, genre, album, source, chemin, statut, cursor, connexion):
        if not le_genre_existe_deja(genre, cursor):
            ajout_du_genre(genre, cursor, connexion)

        genre = recuperation_id_genre(genre, cursor)
        source = recuperation_id_source(source, cursor)
        statut = recuperation_id_utilisateur(statut, cursor)
        cursor.execute("INSERT INTO wav (titre, artiste, genre, album, source, path, utilisateur) VALUES (%s,%s,%s,%s,%s,%s,%s)", (titre, artiste, genre, album,source, chemin, statut))
        connexion.commit()

def le_genre_existe_deja(genre, cursor):
    sql = "SELECT id FROM genre_musicaux WHERE genre = %s" # verifier le nom des champs...
    cursor.execute(sql, (genre,))
    result = cursor.fetchall()
    if len(result) == 0:
        return False
    return True

def ajout_du_genre(genre, cursor, connexion):
    cursor.execute("INSERT INTO genre_musicaux (genre) VALUES (%s)", (genre,))
    connexion.commit()
    print(f"[+] GENRE {genre}")

def recuperation_id_genre(genre, cursor):
    sql = "SELECT id FROM genre_musicaux WHERE genre = %s" # verifier le nom des champs...
    cursor.execute(sql, (genre,))
    result = cursor.fetchall() # [(id1, genre1), (id2, genre1), ...]
    return result[0][0]

def recuperation_id_source(source, cursor):
    sql = "SELECT id FROM sources WHERE source = %s" # verifier le nom des champs...
    cursor.execute(sql, (source,))
    result = cursor.fetchall() # [(id1, genre1), (id2, genre1), ...]
    return result[0][0]

def recuperation_id_utilisateur(statut, cursor):
    sql = "SELECT id FROM users WHERE statut = %s" # verifier le nom des champs...
    cursor.execute(sql, (statut,))
    result = cursor.fetchall() # [(id1, genre1), (id2, genre1), ...]
    return result[0][0]
#----------------------------------------------------------------------------------------------------
#                       pour recuperer les fichiers dans un répertoire
#----------------------------------------------------------------------------------------------------
def extension(path):
    filename, file_extension = os.path.splitext(path)
    return file_extension

def supprimer_mauvaises_extensions(fichiers, bonnes_extensions):
    #print("\n--------------suppression des fichiers non-audios--------------------\n")
    f = deepcopy(fichiers)
    for i in range(len(fichiers)):
        if not extension(fichiers[i]) in bonnes_extensions:
            #print(f"N°<{i+1}>fichier: {fichiers[i]} -> {extension(fichiers[i])} ==> supprimé")
            f.remove(fichiers[i])
    #print("\n-----------------------------------FIN---------------------------------\n")
    return f

def recuperer_les_fichiers_dans_dossier(path, bonnes_extensions):
    for (chemin, dossiers, fichiers) in walk(path):
        if len(fichiers) > 0: # s'il y a des fichiers dans le répertoire:
            #print(f"il y a {len(fichiers)} fichiers dans ce dossier !")
            #print(f"-> {fichiers}")
            Liste_bon_fichiers = supprimer_mauvaises_extensions(fichiers, bonnes_extensions) # on supprime les fichiers qui ne sont pas des audios
            #print(fichiers)
            #print(f"----------------{chemin}------------------\n")
            #print(f"    ==> {dossiers}")
            #print(f"-> [{fichiers}]\n\n")
            return Liste_bon_fichiers
    return False

def recuperer_tous_les_dossiers_dans_un_repertoire(repertoire):
    liste_dossiers= []
    for (chemin, dossiers, fichiers) in walk(repertoire):
        if len(dossiers) == 0:
            print(chemin)
            liste_dossiers.append(chemin)
    return liste_dossiers
    
def avoir_un_dic_de_tous_les_fichiers_dans_repertoire(repertoire, extensions_autorisee):
    d = {}
    dossiers = recuperer_tous_les_dossiers_dans_un_repertoire(repertoire)
    for dossier in dossiers:
        f = recuperer_les_fichiers_dans_dossier(dossier, extensions_autorisee)
        d[dossier] = f
    return d

#----------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------

# https://fr.acervolima.com/extraire-et-ajouter-des-metadonnees-audio-flac-a-laide-du-module-mutagen-en-python/
# https://stackoverflow.com/questions/37400974/unicode-error-unicodeescape-codec-cant-decode-bytes-in-position-2-3-trunca
# https://fr.acervolima.com/acceder-aux-metadonnees-de-divers-formats-de-fichiers-audio-et-video-a-laide-de-python-tinytag-library/

# https://www.delftstack.com/fr/howto/python/python-list-subdirectories/
# https://www.journaldunet.fr/web-tech/developpement/1202869-comment-lister-tous-les-fichiers-d-un-repertoire-en-python/



extensions_autorisee = ['.wav', '.flac', '.mp3']
path = r"stockage_musique"
dic = avoir_un_dic_de_tous_les_fichiers_dans_repertoire(path, extensions_autorisee)
#print(dic)

connexion = bdd_connexion("localhost", "musique", "root", "")
if connexion.is_connected():
    print("connecté à la bdd MySQL !")
cursor = connexion.cursor()

for key in dic.keys():
    #print(f"----------------------{key}-------------------")
    #print(f"{dic[key]}\n")
    chemin = key
    
    for fichier_audio in dic[key]:
        #print(fichier_audio)
        lien_fichier = OS_path.join(chemin, fichier_audio)
        #print(f"\n--------{lien_fichier}----------------")

        if extension(fichier_audio) == ".flac":
            audio = mutagen_FLAC(lien_fichier)

            titre = audio["TITLE"][0]
            artiste = audio["ARTIST"][0]
            genre = audio["GENRE"][0]
            album = audio["ALBUM"][0]

            if il_manque_une_info(genre, artiste):
                if not est_dans_bdd_erreurs(lien_fichier, cursor):
                    ajouter_dans_bdd_des_erreurs(titre, artiste, genre, album,"CD", lien_fichier, "bot", cursor, connexion)
                    print(f"ERREUR FLAC: [{titre}] de {artiste} mis dans bdd problemes...")
                continue
            if not est_dans_bdd(lien_fichier, cursor):
                ajouter_dans_bdd(titre, artiste, genre, album, "CD", lien_fichier, "bot", cursor, connexion)
                print(f"AJOUT FLAC: [{titre}] de {artiste} !")
        
        elif extension(fichier_audio) == ".mp3":
            tags = mutagen_EasyID3(lien_fichier)
            tags_list = tags.keys()
            titre, artiste, genre, album = recuperer_infos_musique_mp3(tags)

            if set(['artist', 'title', 'genre', 'album']).issubset(tags_list):
                if not est_dans_bdd(lien_fichier, cursor):
                    ajouter_dans_bdd(titre, artiste, genre, album, "CD", lien_fichier, "bot", cursor, connexion)
                    print(f"AJOUT MP3: [{titre}] de {artiste} !")

            elif not est_dans_bdd_erreurs(lien_fichier, cursor):
                ajouter_dans_bdd_des_erreurs(titre, artiste, genre, album,"CD", lien_fichier, "bot", cursor, connexion)
                print(f"ERREUR MP3: [{titre}] de {artiste} mis dans bdd problemes...")

        elif extension(fichier_audio) == ".wav":
            print(f"WAV <{fichier_audio}>")
            if not est_dans_bdd_wav(lien_fichier, cursor):
                ajouter_dans_bdd_des_wav(fichier_audio, "unknown", "unknown", "unknown", "CD", lien_fichier, "bot", cursor, connexion)


cursor.close()
connexion.close()
print("MySQL connection is closed")

#https://stackoverflow.com/questions/4040605/does-anyone-have-good-examples-of-using-mutagen-to-write-to-files
#https://fr.from-locals.com/python-mutagen-mp3-id3/