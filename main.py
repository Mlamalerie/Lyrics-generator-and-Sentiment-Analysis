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
        with open('songs/{}/{}_{}_{}.txt'.format('_'.join(artist_name.split(' ')), i+1, album_name, '-'.join(''.join(song_title.split('\'')).split(' '))), 'w') as f:
            f.writelines(lyrics.split('\\n'))


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
    return words[:-1]
        
"""
   
    res = []
    for i in range(len(words)): #pb de double point
        if "." == words[i]:
            if i > 1 and i < len(words):
                if "." == words[i-1]: 
                    res.append(words[i])
        else:
            res.append(words[i])
"""   
    
  

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
        print(mot_vertex)
        if mot_vertex.get_id() == '.':
            
            nbphrase += 1
            nouvellephrase_ok = True
  
        
        
        if (nb_phrases_paragraphes*numparagraphe) == nbphrase and nouvellephrase_ok :
             aventure.append("\n")
             numparagraphe += 1
             
        
    print(aventure)       
    return ' '.join(aventure)
   
    
def main():
        
    words_list = get_words_from_text("text.txt")
    print(words_list)
    G = create_graph(words_list)
    #G.affiche() 
    
    """
    nbphrasemax = int(input(" * Nb phrases maximum > "))
    nbmotmax = int(input("* Nb mot maximum > "))
    para = int(input(" * Nb de paragraphes > "))
    """
    
    resultat = composer(G,words_list,2,6)
    
    print("---")
    for p in resultat.split('.'):
        print(p)
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