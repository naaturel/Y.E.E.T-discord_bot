listeTexte = []
texte = ""
archive = open("channelsID.txt", "r")
for carac in archive:
    texte += carac
    listeTexte.append(texte[18:])
    texte = ""
texte = " ".join(listeTexte)
return texte
     