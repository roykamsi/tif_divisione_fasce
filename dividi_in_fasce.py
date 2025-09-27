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

def pixel_da_mm(mm, dpi=120):
    """Converte millimetri in pixel basandosi sui DPI"""
    return int((mm * dpi) / 25.4)

def calcola_fasce(larghezza, altezza, numero_fasce):
    """Calcola le dimensioni e posizioni delle fasce (colonne verticali)"""
    stampa_step(f"Calcolo divisione in {numero_fasce} fasce verticali...")
    
    larghezza_fascia = larghezza // numero_fasce
    fasce = []
    
    for i in range(numero_fasce):
        x_start = i * larghezza_fascia
        # L'ultima fascia prende tutto il rimanente
        if i == numero_fasce - 1:
            x_end = larghezza
        else:
            x_end = (i + 1) * larghezza_fascia
        
        larghezza_effettiva = x_end - x_start
        
        fasce.append({
            'numero': i + 1,
            'x': x_start,
            'y': 0,
            'larghezza': larghezza_effettiva,
            'altezza': altezza,
            'box': (x_start, 0, x_end, altezza)
        })
        
        print(f"   📐 Fascia {i+1}: {larghezza_effettiva}x{altezza} pixel (X: {x_start}-{x_end})")
    
    stampa_successo(f"Divisione calcolata: {numero_fasce} fasce verticali")
    return fasce

def crea_fascia_con_footer(immagine_fascia, numero_fascia, nome_file, logo, larghezza_fascia, altezza):
    """Crea una fascia con il rettangolo bianco, testo e logo"""
    stampa_step(f"Elaborazione fascia {numero_fascia}...")
    
    # Calcola altezza rettangolo bianco (15mm)
    altezza_footer = pixel_da_mm(15)  # 15mm
    margine_interno = pixel_da_mm(5)  # 5mm
    
    # Crea nuova immagine con spazio aggiuntivo per il footer
    nuova_altezza = altezza + altezza_footer
    immagine_finale = Image.new('RGB', (larghezza_fascia, nuova_altezza), 'white')
    
    # Incolla l'immagine originale
    immagine_finale.paste(immagine_fascia, (0, 0))
    
    # Crea il rettangolo bianco (sovrapposto in basso)
    draw = ImageDraw.Draw(immagine_finale)
    y_footer = altezza - altezza_footer
    draw.rectangle([0, y_footer, larghezza_fascia, nuova_altezza], fill='white', outline=None)
    
    # Prepara il testo
    testo_sx = f"{nome_file} - Parete C{numero_fascia}"
    
    # Carica font (prova diversi font)
    try:
        # Prova font di sistema comuni
        font_size = max(48, int(altezza_footer // 3))  # Font proporzionale all'altezza
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            try:
                font = ImageFont.truetype("Arial.ttf", font_size)
            except:
                try:
                    font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", font_size)
                except:
                    font = ImageFont.load_default()
    except:
        font = ImageFont.load_default()
    
    # Posiziona il testo a sinistra
    centro_footer = y_footer + (altezza_footer // 2)
    y_testo = centro_footer + (font_size * 0.1)  # Sposta leggermente sotto il centro

    # # DEBUG per vedere i valori
    # print(f"   📝 y_footer: {y_footer}")
    # print(f"   📝 altezza_footer: {altezza_footer}")
    # print(f"   📝 centro calcolato: {y_footer + (altezza_footer // 2)}")
    # print(f"   📝 y_testo finale: {y_testo}")

    draw.text((margine_interno, y_testo), testo_sx, fill='black', font=font)

    
    # Ridimensiona e posiziona il logo a destra
    logo_area_larghezza = larghezza_fascia // 1.1  # Mantieni questo
    logo_area_altezza = altezza_footer * 1.1  # DOPPIA l'altezza disponibile (ignora i margini)
    
    # Ridimensiona il logo mantenendo le proporzioni
    logo_ratio = min(logo_area_larghezza / logo.size[0], logo_area_altezza / logo.size[1])
    nuova_larghezza_logo = int(logo.size[0] * logo_ratio)
    nuova_altezza_logo = int(logo.size[1] * logo_ratio)
    
    logo_ridimensionato = logo.resize((nuova_larghezza_logo, nuova_altezza_logo), Image.Resampling.LANCZOS)
    
    # Posiziona il logo in basso a destra
    x_logo = larghezza_fascia - nuova_larghezza_logo - margine_interno
    y_logo = y_footer + margine_interno
    
    # Se il logo ha trasparenza, gestiscila
    if logo_ridimensionato.mode == 'RGBA':
        immagine_finale.paste(logo_ridimensionato, (x_logo, y_logo), logo_ridimensionato)
    else:
        immagine_finale.paste(logo_ridimensionato, (x_logo, y_logo))
    
    print(f"   ✨ Fascia {numero_fascia} elaborata ({larghezza_fascia}x{nuova_altezza} pixel)")
    return immagine_finale

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
            larghezza, altezza = immagine.size
            stampa_successo(f"Immagine caricata - Dimensioni: {larghezza}x{altezza} pixel")
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
        
        # Step 8: Calcola le fasce
        fasce = calcola_fasce(larghezza, altezza, numero_fasce)
        
        print()
        print("🔧 ELABORAZIONE FASCE")
        print("="*25)
        
        # Step 9: Processa ogni fascia
        for i, fascia in enumerate(fasce):
            try:
                # Estrai la porzione dell'immagine
                immagine_fascia = immagine.crop(fascia['box'])
                
                # Crea la fascia con footer
                fascia_finale = crea_fascia_con_footer(
                    immagine_fascia, 
                    fascia['numero'], 
                    nome_file, 
                    logo,
                    fascia['larghezza'],
                    fascia['altezza']
                )
                
                # Salva come PDF (per ora come PNG per test)
                nome_output = f"esportati/{nome_file}_fascia_{fascia['numero']:02d}.png"
                fascia_finale.save(nome_output, "PNG", optimize=False)
                
                stampa_successo(f"Fascia {fascia['numero']} salvata: {nome_output}")
                
            except Exception as e:
                stampa_errore(f"Errore nell'elaborazione della fascia {fascia['numero']}: {e}")
                continue
        
        print()
        stampa_successo(f"Processo completato! {len(fasce)} fasce create nella cartella 'esportati'")
        print("\n📝 Nota: Al momento le fasce sono salvate in PNG. Prossimo step: conversione PDF")
        
    except KeyboardInterrupt:
        print("\n\n👋 Operazione annullata dall'utente.")
    except Exception as e:
        stampa_errore(f"Errore imprevisto: {e}")
        input("\n❌ Premi INVIO per chiudere...")

if __name__ == "__main__":
    main()
    input("\n✨ Premi INVIO per chiudere...")