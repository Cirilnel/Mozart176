import random
import json
from mido import Message, MetaMessage, MidiFile, MidiTrack

# Carica il file JSON delle note
def carica_note():
    with open("notes.json", "r") as file:
        return json.load(file)

TABELLA_MOZART = [
    [96, 22, 141, 41, 105, 122, 11, 30, 70, 121, 26, 9, 112, 49, 109, 14],
    [32, 6, 128, 63, 146, 46, 134, 81, 117, 39, 126, 56, 174, 18, 116, 83],
    [69, 95, 158, 13, 153, 55, 110, 24, 66, 139, 15, 132, 73, 58, 145, 79],
    [40, 17, 113, 85, 161, 2, 159, 100, 90, 176, 7, 34, 67, 160, 52, 170],
    [148, 74, 163, 45, 80, 97, 36, 107, 25, 143, 64, 125, 76, 136, 1, 93],
    [104, 157, 27, 167, 154, 68, 118, 91, 138, 71, 150, 29, 101, 162, 23, 151],
    [152, 60, 171, 53, 99, 133, 21, 127, 16, 155, 57, 175, 43, 168, 89, 172],
    [119, 84, 114, 50, 140, 86, 169, 94, 120, 88, 48, 166, 51, 115, 72, 111],
    [98, 142, 42, 156, 75, 129, 62, 123, 65, 77, 19, 82, 137, 38, 149, 8],
    [3, 87, 165, 61, 135, 47, 147, 33, 102, 4, 31, 164, 144, 59, 173, 78],
    [54, 130, 10, 103, 28, 37, 106, 5, 35, 20, 108, 92, 12, 124, 44, 131]
]

def lancia_dadi():
    return random.randint(1, 6) + random.randint(1, 6)


def genera_composizione(dati_note):
    composizione = []
    for i in range(min(16, len(TABELLA_MOZART))):  
        lancio_dadi = lancia_dadi()  
        indice = lancio_dadi - 2  

        if indice < 0:
            print(f"Indice troppo basso per la riga {i}: {indice}. Imposto a 0.")
            indice = 0  
        if indice >= len(TABELLA_MOZART[i]):
            print(f"Indice troppo alto per la riga {i}: {indice}. Imposto all'ultimo indice valido.")
            indice = len(TABELLA_MOZART[i]) - 1  

        frammento = TABELLA_MOZART[i][indice]  
        print(f"Riga {i + 1}, tiro {lancio_dadi}: scelto frammento {frammento}.")  

        melodia = dati_note[str(frammento)]  
        composizione.append(melodia)
    return composizione

def crea_midi(composizione, nome_file="gioco_dadi_mozart.mid"):
    file_midi = MidiFile()
    traccia_melodia = MidiTrack()  
    traccia_basso = MidiTrack()
    file_midi.tracks.append(traccia_melodia)
    file_midi.tracks.append(traccia_basso)

    tempo = 1000000  
    traccia_melodia.append(MetaMessage('set_tempo', tempo=tempo))  
    traccia_basso.append(MetaMessage('set_tempo', tempo=tempo))    

    traccia_melodia.append(Message('note_on', note=60, velocity=0, time=0))  
    traccia_basso.append(Message('note_on', note=60, velocity=0, time=0))  
    traccia_melodia.append(Message('note_off', note=60, velocity=0, time=1))
    traccia_basso.append(Message('note_off', note=60, velocity=0, time=1))

    
    for melodia in composizione:
        for parte in ['treble', 'bass']:
            if parte in melodia:  
                analizza(melodia[parte], traccia_melodia if parte == 'treble' else traccia_basso)

    file_midi.save(nome_file)


def analizza(note_durata, traccia):
    for nota_durata in note_durata:
        print(f"\nElaborazione gruppo di note/durata: {nota_durata}")  
        if isinstance(nota_durata, list):  
            note_parte = [item for item in nota_durata if isinstance(item, str)]  
            durate = [item for item in nota_durata if isinstance(item, int)]  
            
            if not durate:
                print(f"Errore: nessuna durata trovata per le note {note_parte}. Salto questa parte.")
                continue
            
            durata = durate[0]  
            durata_ticks = int(480 * (4 / durata))  
            print(f"Durata in ticks per tutte le note: {durata} -> {durata_ticks}")  
            
            for nota in note_parte:
                altezza_nota = nota_a_midi(nota)  
                if altezza_nota is None:
                    print(f"Errore: nota '{nota}' non riconosciuta. Ignorata.")
                    continue
                print(f"Nota MIDI: {nota} -> {altezza_nota}")  
                traccia.append(Message('note_on', note=altezza_nota, velocity=64, time=0))  
                traccia.append(Message('note_off', note=altezza_nota, velocity=64, time=durata_ticks)) 
        
        elif isinstance(nota_durata, int):  
            durata_ticks = int(480 * (4 / nota_durata))  
            print(f"Pausa: durata in ticks {nota_durata} -> {durata_ticks}")  
            traccia.append(Message('note_off', note=0, velocity=0, time=durata_ticks))  


def nota_a_midi(nota):
    mappa_note = {
        'c0': 12, 'c#0': 13, 'd0': 14, 'd#0': 15, 'e0': 16, 'f0': 17, 'f#0': 18, 'g0': 19, 'g#0': 20, 'a0': 21, 'a#0': 22, 'b0': 23,
        'c1': 24, 'c#1': 25, 'd1': 26, 'd#1': 27, 'e1': 28, 'f1': 29, 'f#1': 30, 'g1': 31, 'g#1': 32, 'a1': 33, 'a#1': 34, 'b1': 35,
        'c2': 36, 'c#2': 37, 'd2': 38, 'd#2': 39, 'e2': 40, 'f2': 41, 'f#2': 42, 'g2': 43, 'g#2': 44, 'a2': 45, 'a#2': 46, 'b2': 47,
        'c3': 48, 'c#3': 49, 'd3': 50, 'd#3': 51, 'e3': 52, 'f3': 53, 'f#3': 54, 'g3': 55, 'g#3': 56, 'a3': 57, 'a#3': 58, 'b3': 59,
        'c4': 60, 'c#4': 61, 'd4': 62, 'd#4': 63, 'e4': 64, 'f4': 65, 'f#4': 66, 'g4': 67, 'g#4': 68, 'a4': 69, 'a#4': 70, 'b4': 71,
        'c5': 72, 'c#5': 73, 'd5': 74, 'd#5': 75, 'e5': 76, 'f5': 77, 'f#5': 78, 'g5': 79, 'g#5': 80, 'a5': 81, 'a#5': 82, 'b5': 83,
        'c6': 84, 'c#6': 85, 'd6': 86, 'd#6': 87, 'e6': 88, 'f6': 89, 'f#6': 90, 'g6': 91, 'g#6': 92, 'a6': 93, 'a#6': 94, 'b6': 95,
        'c7': 96, 'c#7': 97, 'd7': 98, 'd#7': 99, 'e7': 100, 'f7': 101, 'f#7': 102, 'g7': 103, 'g#7': 104, 'a7': 105, 'a#7': 106, 'b7': 107,
        'c8': 108, 'c#8': 109, 'd8': 110, 'd#8': 111, 'e8': 112, 'f8': 113, 'f#8': 114, 'g8': 115, 'g#8': 116, 'a8': 117, 'a#8': 118, 'b8': 119,
        'c9': 120
    }
    return mappa_note.get(nota, None)

def main():
    dati_note = carica_note()
    composizione = genera_composizione(dati_note)
    crea_midi(composizione)

if __name__ == "__main__":
    main()
