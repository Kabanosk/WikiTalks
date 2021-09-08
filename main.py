import wikipedia
import pyttsx3
import re
import speech_recognition as sr


def listening_the_question(language):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        if language == 'pl':
            try:
                print("Zadaj pytanie zaczynające się od \"Co to jest...\" lub powiedz szukaną frazę.")
                audio = recognizer.listen(source)
                text = recognizer.recognize_google(audio, language='pl-PL')
                print(text)
                return text
            except:
                print('Wybacz nie udało mi się ciebie usłyszeć. '
                      'Czy chcesz spróbować jescze raz?')
                text = recognizer.recognize_google(audio, language='pl-PL')
                if text.replace(' ', '') == 'tak':
                    listening_the_question('pl')
                else : return None
        elif language == 'en':
            try:
                print("Ask a question which start with \"What is...\" or say a search term.")
                audio = recognizer.listen(source)
                text = recognizer.recognize_google(audio)
                return text
            except:
                print('I am so sorry, but I cannot hear you. '
                      'Do you want to try again?')
                text = recognizer.recognize_google(audio)
                if text.replace(' ', '') == 'yes':
                    listening_the_question('en')
                else : return None

def answering_the_question(language, title):
    wiki = Wikipedia(language, title)
    engine = pyttsx3.init()
    engine.setProperty('rate', 130)
    engine.say(wiki.desc)
    engine.runAndWait()

def changing_question_to_searching_phrase(language, question):
    if language == 'pl':
        question = re.sub("Co to jest ", "", question)
        question = re.sub("co to jest ", "", question)
        question = re.sub("Co to ", "", question)
        question = re.sub("co to ", "", question)
        return question
    elif language == 'en':
        question = re.sub("What is ", "", question)
        question = re.sub("what is ", "", question)
        return question

class Wikipedia:
    def __init__(self, language, searching_phrase):
        assert language
        assert type(searching_phrase) == str
        wikipedia.set_lang(language)
        self.language = language
        self.searching_phrase = searching_phrase
        self.desc = self.description_in_wikipedia(searching_phrase)

    def description_in_wikipedia(self, string):
        page = wikipedia.page(string)
        assert page
        content = page.content
        assert content
        description = ''
        for i in range(len(content)):
            if content[i:i + 2] == '.\n':
                description = content[:i + 1]
                break
        if '.\n' not in content:
            return None
        return self.deleting_special_symbols(description)

    @staticmethod
    def deleting_special_symbols(text):
        text = text.replace('\n', '')
        text = re.sub(r"\([^()]*\)", "", text)
        text = re.sub(r"\{[^{}]*\}", "", text)
        text = re.sub(r"\s+", " ", text)
        return text

def initialize():
    language = input('What is your preferred language?/Jaki jest twój preferowany język? (en/pl)')
    question = listening_the_question(language)
    sp = changing_question_to_searching_phrase(language, question)
    answering_the_question(language, sp)


initialize()
