import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(f"done/File 1.json", "r", encoding="utf-8") as f:
    data = json.load(f)

    recognizedPhrases = data['recognizedPhrases']
    texto = []
    silencios = []

    for loop in range(0, len(recognizedPhrases)):
        words = recognizedPhrases[loop]['nBest'][0]['words']
        frase = f"{words[0]['word']} "

        for pos in range(0, len(words)):
            appended = False
            atual = words[pos]
            anterior = words[pos - 1]

            fim_anterior = anterior["offsetMilliseconds"] + anterior["durationMilliseconds"]
            inicio_atual = atual["offsetMilliseconds"]
            
            silencio = inicio_atual - fim_anterior
            if silencio <= 500:
                frase += f"{words[pos]['word']} "
            else:
                texto.append(frase)
                appended = True
                frase = f"{words[pos]['word']} "

            if pos == (len(words)-1) and not appended:          
                texto.append(frase) 
                
    for frases in texto:
       print(frases)

    #        print("Silêncios entre palavras:", silencios)


        # if float(offset) < 1000:
        #     frase += f"{word['word']} "
        #     print(frase)
        # else:
        #     frase = f"{word['word']} "
        #     print(frase)

        
        
