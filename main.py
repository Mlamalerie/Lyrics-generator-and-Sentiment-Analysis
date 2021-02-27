# -*- coding: utf-8 -*-
import os
import string
import random
from graph import Graph, Vertex

import lyricsgenius
genius = lyricsgenius.Genius("dj04TpKhldHudO8VnobaSSzXtuuZ2hbSgl1DW-1Jug6i1Tt33B0JjXhDzdAk6V7m")

def save_lyrics(songs, artist_name, album_name):
    for i in range(len(songs)):
        song_title = songs[i]
        song = genius.search_song(song_title, artist_name)
        lyrics = song.lyrics
        nomEmplacementSauvegarde = "songs"
        if not os.path.exists(nomEmplacementSauvegarde):
            os.makedirs(nomEmplacementSauvegarde)
        nomEmplacementSauvegarde += "/" + '_'.join(artist_name.split(' '))
        if not os.path.exists(nomEmplacementSauvegarde):
            os.makedirs(nomEmplacementSauvegarde)
        with open('lyrics/{}/{}_{}_{}.txt'.format('_'.join(artist_name.split(' ')), i+1, album_name, '-'.join(''.join(song_title.split('\'')).split(' '))), 'w') as f:
            f.writelines(lyrics.split('\\n'))

def retirerDoublons(li,doublonslistesuppr):
    res = []
    i = 0
    
    while i < len(li):
        if li[i] in doublonslistesuppr:
            k = 1
            res.append(li[i])
            if i+k < len(li):
                while li[i+k] in doublonslistesuppr:
                    k += 1
                    if i+k >= len(li):
                        break
        else:
            k = 1
            res.append(li[i])
        i += k
    return res

def get_words_from_text(text_chemin):
    with open(text_chemin, 'rb') as file:
        text = file.read().decode("utf-8") #read
        text = text.lower()
        #print(len(text.split('\n')))
        #text = ' .'.join(text.split('\n'))
        
        text = ' . '.join(text.split('\n'))
        
        #delete punctuation
        illegal_punc = list(string.punctuation)
        legal_punc = ['-','.','!']
        for c in legal_punc:
            illegal_punc.remove(c)
        illegal_punc = ''.join(illegal_punc)
        
        #remove ponctuation
        text = text.translate(str.maketrans('', '', illegal_punc)) 
        text = ' .'.join(text.split('.')) # add ponctuation
        
    words = text.split()
    words = retirerDoublons(words,['.'])
    return words


def create_graph(words_list):
    G = Graph()
    prec_mot = None
    
    for mot in words_list:
        # verifie si le mot est dans le graph, et sinon il l'ajoute dans le graph
        mot_vertex = G.get_vertex(mot)
        
        # si il existe un mot précédent alors on ajoute à la suite 
        if prec_mot: # prec_mot est un vertex
            prec_mot.increment_edge(mot_vertex) # (prec_mot) -- ++ -- (mot_vertex)
        else:
            print("!")
            
        prec_mot = mot_vertex
        
    G.generate_all_informations()    
    #G.affiche()
    return G
    
def composer(G,words_list,nb_phrases_paragraphes, nbmaxphrases,nbmaxmots=1000):
    aventure = []
    # choisir un mot de commencement aléatoire, se positionner sur son vortex 
    
    words_list = [x for x in words_list if x != '.']
    debut = random.choice(words_list)
    
    mot_vertex = G.get_vertex(debut)
   
    numparagraphe = 1
    nbphrase, nbmot= 0,0
    while nbphrase < nbmaxphrases and nbmot < nbmaxmots:
        aventure.append(mot_vertex.id)
        mot_vertex = G.get_next_word(mot_vertex)
        
        nbmot += 1
        nouvellephrase_ok = False
        #print(mot_vertex)
        if mot_vertex.get_id() == '.':
            
            nbphrase += 1
            nouvellephrase_ok = True
  
        
        
        if (nb_phrases_paragraphes*numparagraphe) == nbphrase and nouvellephrase_ok :
             aventure.append("\n")
             numparagraphe += 1
             
        
    #☺print(aventure)       
    return ' '.join(aventure)

import datetime

def printresultat(resultat,nom):
    
    nomEmplacementSauvegarde = "results"
    if not os.path.exists(nomEmplacementSauvegarde):
    	os.makedirs(nomEmplacementSauvegarde)
    chemin = nomEmplacementSauvegarde
    
    dateajd = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
  
    chemin += "/result_" + nom + "_"
    chemin += dateajd
    chemin += ".txt"
    with open(chemin,"a") as fic: #creer fichier txt
        print("---")
        for p in resultat.split('.'):

            fic.write(p + '\n') 
        
    print(" * The generated words are saved :",chemin,"!")

def select_files(orig,i = 0,prof=1,select_dic = {}):
    espace = "  | "*prof
    
    audioext = ['.mp3','.wav','.ogg']

    if os.path.exists(str(orig)):
        listefichiers = os.listdir(orig)
        for fil in listefichiers:
            fil = orig + "\\" + fil
            if os.path.isdir(fil): #si dossier
                print(espace,"---",orig.split("\\")[-1], prof)
                i = select_files(fil,i,prof+1,select_dic)    
            else: # si fichier
                
                
                bay, ext = os.path.splitext(fil)
                if ext in audioext: #si fichier audio
                    print( espace," :",fil.split("\\")[-1])
                    ecouter(fil)
                    
                    
                   
                select_dic[i] = fil
                i+=1
              
       
        return i
    
   


def main():
    print("////////////////////////////")
    print("/////// * LYRIC GENERATOR *")
    print("//////")
    choix = {}
    dossierdata = "lyrics"
    for i, artistdir in enumerate(os.listdir(dossierdata)):
        choix[i] = dossierdata + "/" + artistdir
        print("/"*(len(os.listdir("lyrics"))*2-i) + " {} - {} ".format(i,artistdir))
        
    c = int(input(" > "))
    print(choix)
    fichier = choix[c]
    
    words_list = get_words_from_text(fichier)
    print(words_list[0:20])
    G = create_graph(words_list)
    #G.affiche() 
    
    """
    nbphrasemax = int(input(" * Nb phrases maximum > "))
    nbmotmax = int(input("* Nb mot maximum > "))
    para = int(input(" * Nb de paragraphes > "))
    """
    
    resultat = composer(G,words_list,4,25)
    
    printresultat(resultat,fichier.split(".")[0])
    """   
    c = int(input("\n (0 : CONTINUE)   (1 : QUIT) > "))
    if c == 0:
        main()
    """
  
main() 
"""    
if __name__ == '__main__':
    songs = [
       
        '94','pleure pas','Arrete ta flute',"regrette","testament","les choses simples","message a la racaille"
    ]
    save_lyrics(songs, 'Rohff', '')

"""