from collections import Counter
import spacy

class WordProcessor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def processPoint(self, text: str) -> list[str]:
        doc = self.nlp(text) 
        return [chunk.text for chunk in doc.noun_chunks]

    def processData(self, data: list[list[str]], count: int):
        processedPoints = []
        for pt in data:
            processedPoints.extend(self.processPoint(pt))
        
        phraseCount = Counter(processedPoints)
        mostCommon = phraseCount.most_common(count)

        res = []
        for pair in mostCommon:
            obj = {
                'phrase': pair[0],
                'count': pair[1]
            }
            res.append(obj)
        return res


