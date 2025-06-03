import unittest
from add_sounds import AudioProcessor

class TestSplitIntoSentences(unittest.TestCase):
    def setUp(self):
        self.processor = AudioProcessor()

    def test_split_into_sentences_basic(self):
        text = "Hello world! How are you? I am fine."
        expected = ["Hello world!", "How are you?", "I am fine."]
        result = self.processor._split_into_sentences(text)
        self.assertEqual(result, expected)

    def test_split_into_sentences_with_commas(self):
        text = "This is a test, and it works well."
        expected = ["This is a test,", "and it works well."]
        result = self.processor._split_into_sentences(text)
        self.assertEqual(result, expected)

    def test_split_into_sentences_with_multiple_punctuation(self):
        text = "Wait... What? Really?!"
        expected = ["Wait...", "What?", "Really?!"]
        result = self.processor._split_into_sentences(text)
        self.assertEqual(result, expected)

    def test_split_into_sentences_with_extra_spaces(self):
        text = "  Hello world!   How are you?  "
        expected = ["Hello world!", "How are you?"]
        result = self.processor._split_into_sentences(text)
        self.assertEqual(result, expected)

    def test_split_into_sentences_empty_string(self):
        text = ""
        expected = []
        result = self.processor._split_into_sentences(text)
        self.assertEqual(result, expected)

    def test_split_into_sentences_no_punctuation(self):
        text = "This is a test"
        expected = ["This is a test"]
        result = self.processor._split_into_sentences(text)
        self.assertEqual(result, expected)

    def test_split_into_sentences_only_punctuation(self):
        text = "...!?"
        expected = ["...!?"]
        result = self.processor._split_into_sentences(text)
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()