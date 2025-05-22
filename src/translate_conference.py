import tkinter as tk
from tkinter import messagebox
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
import os
import time
from pydub import AudioSegment

load_dotenv()

class AzureSpeechTranslator:
    def __init__(self, chave, regiao, idioma_origem, idioma_destino):
        self.chave = chave
        self.regiao = regiao
        self.idioma_origem = idioma_origem
        self.idioma_destino = idioma_destino

    def escutar_e_traduzir(self):
        translation_config = speechsdk.translation.SpeechTranslationConfig(
            subscription=self.chave,
            region=self.regiao
        )
        translation_config.speech_recognition_language = self.idioma_origem
        translation_config.add_target_language(self.idioma_destino)

        audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)

        translator = speechsdk.translation.TranslationRecognizer(
            translation_config=translation_config,
            audio_config=audio_config
        )

        resultado = translator.recognize_once()

        if resultado.reason == speechsdk.ResultReason.TranslatedSpeech:
            return resultado.translations[self.idioma_destino]
        elif resultado.reason == speechsdk.ResultReason.RecognizedSpeech:
            return resultado.text
        return None

class AzureTextToSpeech:
    def __init__(self, chave, regiao, voz):
        self.chave = chave
        self.regiao = regiao
        self.voz = voz

    def sintetizar_e_reproduzir_salvar(self, texto, filename):
        speech_config = speechsdk.SpeechConfig(
            subscription=self.chave,
            region=self.regiao
        )
        speech_config.speech_synthesis_voice_name = self.voz

        # Salva em arquivo
        audio_config_file = speechsdk.audio.AudioOutputConfig(filename=filename)
        synthesizer_file = speechsdk.SpeechSynthesizer(
            speech_config=speech_config,
            audio_config=audio_config_file
        )
        result = synthesizer_file.speak_text_async(texto).get()

        if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
            raise Exception("Erro ao sintetizar áudio.")

        # Reproduz
        audio_config_speaker = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
        synthesizer_speaker = speechsdk.SpeechSynthesizer(
            speech_config=speech_config,
            audio_config=audio_config_speaker
        )
        synthesizer_speaker.speak_text_async(texto).get()

class AppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Conversa Bilíngue com Azure")
        self.root.geometry("600x600")

        self.chave = os.getenv("SUBSCRIPTION_KEY")
        self.regiao = os.getenv("REGION")

        if not self.chave or not self.regiao:
            messagebox.showerror("Erro", "Configure SUBSCRIPTION_KEY e REGION no .env")
            self.root.destroy()
            return

        self.idiomas = {
            "Português (Brasil)": "pt-BR",
            "Inglês (EUA)": "en-US",
            "Espanhol": "es-ES",
            "Francês": "fr-FR",
            "Alemão": "de-DE",
            "Italiano": "it-IT",
            "Japonês": "ja-JP",
            "Coreano": "ko-KR"
        }

        self.vozes = {
            "pt-BR": "pt-BR-FranciscaNeural",
            "en-US": "en-US-JennyNeural",
            "es-ES": "es-ES-ElviraNeural",
            "fr-FR": "fr-FR-DeniseNeural",
            "de-DE": "de-DE-KatjaNeural",
            "it-IT": "it-IT-ElsaNeural",
            "ja-JP": "ja-JP-NanamiNeural",
            "ko-KR": "ko-KR-SunHiNeural"
        }

        frame_pessoa1 = tk.Frame(root)
        frame_pessoa1.pack(pady=5)

        tk.Label(frame_pessoa1, text="Pessoa 1 - Idioma:").pack(side=tk.LEFT, padx=5)

        self.idioma1_var = tk.StringVar(value="pt-BR")
        tk.OptionMenu(frame_pessoa1, self.idioma1_var, *self.idiomas.values()).pack(side=tk.LEFT)

        frame_pessoa2 = tk.Frame(root)
        frame_pessoa2.pack(pady=5)
        
        tk.Label(frame_pessoa2, text="Pessoa 2 - Idioma:").pack(side=tk.LEFT, padx=5)
        self.idioma2_var = tk.StringVar(value="en-US")
        tk.OptionMenu(frame_pessoa2, self.idioma2_var, *self.idiomas.values()).pack(side=tk.LEFT)

        tk.Label(root, text="Histórico da Conversa:").pack(pady=5)
        scrollbar = tk.Scrollbar(root)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.history_listbox = tk.Listbox(root, width=80, height=15, yscrollcommand=scrollbar.set)
        self.history_listbox.pack(pady=5)
        scrollbar.config(command=self.history_listbox.yview)

        self.status_label = tk.Label(root, text="Status: Aguardando...", fg="blue")
        self.status_label.pack(pady=10)

        frame_speak = tk.Frame(root)
        frame_speak.pack(pady=10)
        
        self.pessoa1_button = tk.Button(frame_speak, text="Pessoa 1 Falar", command=self.pessoa1_fala, font=("Arial", 12))
        self.pessoa1_button.pack(side=tk.LEFT, padx=20)
        
        self.pessoa2_button = tk.Button(frame_speak, text="Pessoa 2 Falar", command=self.pessoa2_fala, font=("Arial", 12))
        self.pessoa2_button.pack(side=tk.LEFT)

        frame_save = tk.Frame(root)
        frame_save.pack(pady=10)

        self.export_button = tk.Button(frame_save, text="Exportar Histórico", command=self.exportar_historico).pack(side=tk.LEFT,padx=20)

        self.concat_audio_button = tk.Button(frame_save, text="Concatenar Áudios", command=self.concatenar_audios).pack(pady=10)

        self.historico = []
        self.audio_files = []
        self.audio_count = 0

    def processar_fala(self, quem):
        self.status_label.config(text=f"{quem}: Gravando...", fg="orange")
        self.root.update()

        idioma1 = self.idioma1_var.get()
        idioma2 = self.idioma2_var.get()

        if quem == "Pessoa 1":
            translator = AzureSpeechTranslator(self.chave, self.regiao, idioma1, idioma2)
            voz = self.vozes.get(idioma2, f"{idioma2}-Neural")
            origem = idioma1
            destino = idioma2
        else:
            translator = AzureSpeechTranslator(self.chave, self.regiao, idioma2, idioma1)
            voz = self.vozes.get(idioma1, f"{idioma1}-Neural")
            origem = idioma2
            destino = idioma1

        tts = AzureTextToSpeech(self.chave, self.regiao, voz=voz)

        self.status_label.config(text=f"{quem}: Traduzindo...", fg="purple")
        self.root.update()

        try:
            traducao = translator.escutar_e_traduzir()
            if traducao:
                self.status_label.config(text=f"{quem}: Reproduzindo...", fg="green")
                self.root.update()
                self.audio_count += 1
                filename = f"temp_audio_{self.audio_count}.wav"
                self.audio_files.append(filename)
                tts.sintetizar_e_reproduzir_salvar(traducao, filename)
                time.sleep(1)

                msg = f"{quem} ({origem}) → ({destino}): {traducao}"
                self.historico.append(msg)
                self.history_listbox.insert(tk.END, msg)
                self.status_label.config(text="Status: Aguardando...", fg="blue")
            else:
                self.status_label.config(text=f"{quem}: Nenhuma fala reconhecida.", fg="red")
        except Exception as e:
            messagebox.showerror("Erro", str(e))
            self.status_label.config(text=f"Erro: {e}", fg="red")

    def pessoa1_fala(self):
        self.processar_fala("Pessoa 1")

    def pessoa2_fala(self):
        self.processar_fala("Pessoa 2")

    def exportar_historico(self):
        with open("historico_conversa.txt", "w", encoding="utf-8") as f:
            for linha in self.historico:
                f.write(linha + "\n")
        messagebox.showinfo("Exportação", "Histórico exportado para 'historico_conversa.txt'")

    def concatenar_audios(self):
        if not self.audio_files:
            messagebox.showwarning("Aviso", "Nenhum áudio para concatenar.")
            return

        combined = AudioSegment.empty()
        for file in self.audio_files:
            combined += AudioSegment.from_file(file)

        combined.export("conversa_final.wav", format="wav")
        messagebox.showinfo("Concatenação", "Áudios concatenados em 'conversa_final.wav'.")

if __name__ == "__main__":
    root = tk.Tk()
    app = AppGUI(root)
    root.mainloop()
