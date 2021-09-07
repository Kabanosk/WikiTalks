import wikipedia
import pyttsx3
import re


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


def answering_the_question(language, title):
    wiki = Wikipedia(language, title)
    engine = pyttsx3.init()
    engine.setProperty('rate', 135)
    engine.say(wiki.desc)
    engine.runAndWait()


tmp_language = 'en'
tmp_title = 'Recursive Neutral Network'
answering_the_question(tmp_language, tmp_title)