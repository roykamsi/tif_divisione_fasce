#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script per dividere immagini TIF in fasce e esportare in PDF
Versione 1.0 - Base
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont
import math

def stampa_step(messaggio):
    """Stampa un messaggio con formatting per gli step"""
    print(f"🔄 {messaggio}")

def stampa_successo(messaggio):
    """Stampa un messaggio di successo"""
    print(f"✅ {messaggio}")

def stampa_errore(messaggio):
    """Stampa un messaggio di errore"""
    print(f"❌ ERRORE: {messaggio}")

def trova_file_tif():
    """Trova il file TIF nella directory corrente"""
    stampa_step("Ricerca file TIF nella directory corrente...")
    
    file_tif = None
    for file in os.listdir('.'):
        if file.lower().endswith('.tif') or file.lower().endswith('.tiff'):
            if file_tif is None:
                file_tif = file
                stampa_successo(f"File TIF trovato: {file}")
            else:
                stampa_errore("Trovati più file TIF. Tieni solo un file TIF nella cartella.")
                return None
    
    if file_tif is None:
        stampa_errore("Nessun file TIF trovato nella directory corrente.")
        return None
    
    return file_tif

def controlla_logo():
    """Controlla se esiste il file logo_fasce.jpg"""
    stampa_step("Controllo presenza logo_fasce.jpg...")
    
    if not os.path.exists('logo_fasce.jpg'):
        stampa_errore("File 'logo_fasce.jpg' non trovato nella directory corrente.")
        return False
    
    stampa_successo("Logo trovato: logo_fasce.jpg")
    return True

def ottieni_numero_fasce():
    """Chiede all'utente il numero di fasce"""
    while True:
        try:
            stampa_step("Inserimento numero di fasce...")
            numero = input("\n📝 Inserisci il numero di fasce da creare: ")
            numero_fasce = int(numero)
            
            if numero_fasce <= 0:
                print("⚠️  Il numero deve essere maggiore di 0. Riprova.")
                continue
            
            stampa_successo(f"Numero di fasce impostato: {numero_fasce}")
            return numero_fasce
            
        except ValueError:
            print("⚠️  Inserisci un numero valido. Riprova.")
        except KeyboardInterrupt:
            print("\n\n👋 Operazione annullata dall'utente.")
            sys.exit(0)

def crea_cartella_esportati():
    """Crea la cartella 'esportati' se non esiste"""
    stampa_step("Preparazione cartella di output...")
    
    if not os.path.exists('esportati'):
        os.makedirs('esportati')
        stampa_successo("Cartella 'esportati' creata")
    else:
        stampa_successo("Cartella 'esportati' già esistente")

def main():
    """Funzione principale"""
    print("="*60)
    print("🖼️  SCRIPT DIVISIONE IMMAGINI TIF IN FASCE")
    print("="*60)
    print()
    
    try:
        # Step 1: Trova il file TIF
        file_tif = trova_file_tif()
        if not file_tif:
            input("\n❌ Premi INVIO per chiudere...")
            return
        
        # Step 2: Controlla il logo
        if not controlla_logo():
            input("\n❌ Premi INVIO per chiudere...")
            return
        
        # Step 3: Ottieni nome file senza estensione
        nome_file = os.path.splitext(file_tif)[0]
        stampa_successo(f"Nome file (senza estensione): {nome_file}")
        
        # Step 4: Chiedi numero di fasce
        numero_fasce = ottieni_numero_fasce()
        
        # Step 5: Crea cartella output
        crea_cartella_esportati()
        
        # Step 6: Carica l'immagine TIF
        stampa_step(f"Caricamento dell'immagine {file_tif}...")
        try:
            immagine = Image.open(file_tif)
            stampa_successo(f"Immagine caricata - Dimensioni: {immagine.size[0]}x{immagine.size[1]} pixel")
        except Exception as e:
            stampa_errore(f"Impossibile aprire l'immagine: {e}")
            input("\n❌ Premi INVIO per chiudere...")
            return
        
        # Step 7: Carica il logo
        stampa_step("Caricamento logo...")
        try:
            logo = Image.open('logo_fasce.jpg')
            stampa_successo(f"Logo caricato - Dimensioni: {logo.size[0]}x{logo.size[1]} pixel")
        except Exception as e:
            stampa_errore(f"Impossibile aprire il logo: {e}")
            input("\n❌ Premi INVIO per chiudere...")
            return
        
        print()
        print("🎯 INIZIO PROCESSO DI DIVISIONE")
        print("="*40)
        
        # TODO: Implementare il processo di divisione
        stampa_step("Processo di divisione non ancora implementato...")
        print("📋 Prossimi step da implementare:")
        print("   - Calcolo dimensioni fasce")
        print("   - Divisione immagine")
        print("   - Aggiunta rettangolo bianco e testo")
        print("   - Inserimento logo")
        print("   - Esportazione PDF")
        
        print()
        stampa_successo("Script completato con successo! (versione base)")
        
    except KeyboardInterrupt:
        print("\n\n👋 Operazione annullata dall'utente.")
    except Exception as e:
        stampa_errore(f"Errore imprevisto: {e}")
        input("\n❌ Premi INVIO per chiudere...")

if __name__ == "__main__":
    main()
    input("\n✨ Premi INVIO per chiudere...")