"""Voice controller: text I/O fallback when audio hardware unavailable."""


class VoiceController:
    def __init__(self, use_audio: bool = False):
        self.use_audio = use_audio
        self.recognizer = None
        self.engine = None
        if use_audio:
            try:
                import speech_recognition as sr
                import pyttsx3
                self.recognizer = sr.Recognizer()
                self.engine = pyttsx3.init()
            except (ImportError, Exception):
                self.use_audio = False

    def listen(self) -> str:
        if self.use_audio and self.recognizer:
            import speech_recognition as sr
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source)
            return self.recognizer.recognize_google(audio)
        return input("You > ")

    def speak(self, text: str):
        if self.use_audio and self.engine:
            self.engine.say(text)
            self.engine.runAndWait()
        else:
            print(f"FRIDAY > {text}")
