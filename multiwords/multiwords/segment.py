import plp
import re
from collections import defaultdict


class Multisegment(plp.PLP):
    """
    Class resposible for multisegment word searching
    """
    def __init__(self, filename):
        plp.PLP.__init__(self, filename)
        self.types = set([])
        self.longest = 5
        #list of polish vowels
        self.vowels = {'a', 'ą', 'e', 'ę', 'y', 'u', 'i', 'o', 'ó'}

    def case(self, word):
        """
        Returns the case of a type of word
        """
        for k, v in self.fvec(self.rec(word)[0]).items():
            if v == word:
                return k
        return 0

    def type(self, word):
        """Returns the the type
        A. nouns
        B. verbs
        C. adjectives
        D. numerals
        E. pronoun
        F. adverb
        G. non-changeable words
        H. segments
        I. shorts
        O. other
        """
        word = word.replace(".", "")
        found_id = self.rec(word)
        if len(found_id) and self.label(found_id[0])[0] == 'A':
            return self.label(found_id[0])[0] + str(self.case(word))
        elif len(found_id):
            return self.label(found_id[0])[0]
        else:
            # if it is not recognised by plp
            if word[len(word) - 1] in self.vowels:
                return "C"
            elif word[len(word) - 1].isdigit():
                return "D"
            else:
                return "A1"

    @staticmethod
    def find_words(lines):
        """Returns a generator analysing list of lines"""
        for line in lines:
            yield re.findall("[A-Z0-9a-zóęąśłżźćńĘÓĄŚŁŻŹĆŃ,\.]+", line, re.UNICODE)

    def load_classes_from_file(self, classfile):
        """
        Gets multi-segment word's classes from a file
        """
        lines = open(classfile).readlines()

        # check all
        for segment in self.find_words(lines):
            result = [self.type(word.lower()) for word in segment]
            self.types.add("".join(result))

        return self.types

    def load_classes(self, types_set):
        self.types = types_set

    def get_next_plausible(self, i, analyzed):
        """
        Gets the next existing segment
        """
        start = ""
        # We seek starting in "i" in "analyzed" list of words
        j_id = i
        for j in analyzed[i:min(i + self.longest, len(analyzed))]:
            j_id += 1
            # get rid of , and .
            start += self.type(j.lower().replace(",", "").replace(".", ""))
            stop = False
            # check if a . or , is in word - if so then there is not a multi-segment word further
            if ',' in j or '.' in j:
                stop = True
                # check if exists
            if start in self.types:
                return analyzed[i:j_id]   # .start
                # if we need to stop and found nothing
            if stop:
                return None

        return None

    def find_candidates(self, filename):
        """
        Finds the candidates that could be multi-segment words in a file. Returns a generator.
        """

        tests = open(filename)
        lines = tests.read()

        analyzed = next(self.find_words([lines]))

        for i in range(0, len(analyzed)):
            row = self.get_next_plausible(i, analyzed)
            if row:
                yield " ".join(row).lower().replace(",", "").replace(".", "")

    def find_candidates_in_files(self, filenames):
        candidates = defaultdict(int)
        words = set([])
        for i in filenames:
            for j in self.find_candidates(i):
                candidates[j] += 1
                for word in j.split(" "):
                    tmp = self.rec(word)
                    if len(tmp) > 0:
                        words.add(self.bform(tmp[0]))
                    else:
                        words.add(word)
        return candidates, words

    def find_base(self, word):
        tmp = self.rec(word)
        if len(tmp) > 0:
            return self.bform(tmp[0])
        else:
            return word