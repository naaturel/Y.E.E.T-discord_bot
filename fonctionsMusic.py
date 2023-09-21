def archiverMusic(fichier, ajout):
    archive = open(fichier, "a")
    archive.write(f"{ajout}\n")
    archive.close()