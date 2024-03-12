class Editor:
    def __init__(self, text=''):
        self._text = text

    def type(self, new_text):
        self._text += new_text

    def save(self):
        return Snapshot(self, self._text)

    def restore(self, snapshot):
        self._text = snapshot.get_state()

    def __str__(self):
        return self._text


class Snapshot:
    def __init__(self, editor, text):
        self._editor = editor
        self._text = text

    def get_state(self):
        return self._text

    def restore(self):
        self._editor.restore(self)


if __name__ == "__main__":
    editor = Editor()
    editor.type("This is the first sentence.")
    editor.type(" This is second.")

    # Зберігаємо стан
    saved = editor.save()

    editor.type(" And this is third.")
    print(f"Current text: {editor}")

    # Відновлюємо до попереднього збереженого стану
    editor.restore(saved)
    print(f"After restoration: {editor}")
