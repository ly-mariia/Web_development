class TextComponent:
    def get_text(self):
        pass

    def set_text(self, text):
        pass


class BasicText(TextComponent):
    def __init__(self, text=''):
        self._text = text

    def get_text(self):
        return self._text

    def set_text(self, text):
        self._text = text


class TextDecorator(TextComponent):
    def __init__(self, component):
        self._component = component

    def get_text(self):
        return self._component.get_text()

    def set_text(self, text):
        self._component.set_text(text)


class UpperCaseDecorator(TextDecorator):
    def get_text(self):
        return self._component.get_text().upper()


class HTMLDecorator(TextDecorator):
    def get_text(self):
        return f"<p>{self._component.get_text()}</p>"


# Створюємо базовий текст
basic_text = BasicText("hello, world")

# "Обгортаємо" базовий текст, щоб перевести його у верхній регістр
upper_text = UpperCaseDecorator(basic_text)

# Тепер "обгортаємо" текст із верхнім регістром у HTML теги
html_text = HTMLDecorator(upper_text)

print(basic_text.get_text())  # Виводить: hello, world
print(upper_text.get_text())  # Виводить: HELLO, WORLD
print(html_text.get_text())   # Виводить: <p>HELLO, WORLD</p>
