def archiver(fichier, ajout):
    archive = open(fichier, "r")
    roomID = int(ajout[:18])
    listage = []
    verif = []
    indexVerif = ""
    listage = lister("channelsID.txt", listage)
    for element in listage:
        for i, carac in enumerate(element):
            if i <= 17:
                indexVerif += carac
        verif.append(int(indexVerif))
        indexVerif = ""
    archive.close()
    if roomID not in verif:
        archive = open(fichier, "a")
        archive.write(f"{ajout[:18]} #{len(verif) + 1} : {ajout[18:]}\n")
    archive.close()

def lister(fichier, liste):
    liste = []
    archive = open(fichier, "r")
    for ligne in archive:
        liste.append(ligne)
    return liste

def recupChannelsID ():
    listeTexte = []
    texte = ""
    archive = open("channelsID.txt", "r")
    for carac in archive:
        texte += carac
        listeTexte.append(texte[18:])
        texte = ""
    texte = " ".join(listeTexte)
    return texte