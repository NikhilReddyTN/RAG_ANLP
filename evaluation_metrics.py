import re
import json
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def standardize(str1, str2, stops):
    str1 = str1.lower()
    str2 = str2.lower()

    text1 = re.sub(r'[^\w\s]', '', str1)
    text1 = re.sub(r'\s+', ' ', text1).strip()

    text2 = re.sub(r'[^\w\s]', '', str2)
    text2 = re.sub(r'\s+', ' ', text2).strip()

    stopWords = set(stopwords.words('english'))
    word1 = word_tokenize(text1)
    word2 = word_tokenize(text2)

    word1 = [w for w in word1 if w not in stopWords]
    word2 = [w for w in word2 if w not in stopWords]

    return word1, word2


def metrics(json1, json2):
    nltk.download('stopwords')
    stops = set(stopwords.words('english'))

    with open(json1, "r", encoding="utf-8") as file1:
        answers = json.load(file1)
    with open(json2, "r", encoding="utf-8") as file2:
        expected = json.load(file2)
    
    exact_matches = 0
    f1_scores = []
    ans_recall = []
    total_checks = len(expected)
    for num in answers:
        word1, word2 = standardize(answers[num][0], expected[num])
        if "".join(word1) == "".join(word2):
            exact_matches += 1

        overlapping = 0
        for w in word1:
            if w in word2:
                overlapping += 1
        
        precision = overlapping / len(word1) if word1 else 0
        recall = overlapping / len(word2) if word2 else 0
        ans_recall.append(recall)

        f1 = (2 * precision * recall) / (precision + recall) if precision + recall != 0 else 0
        f1_scores.append(f1)
    
    em = exact_matches / total_checks
    avg_f1_scores = sum(f1_scores) / len(f1_scores) if f1_scores else 0
    avg_recall = sum(ans_recall) / len(ans_recall) if ans_recall else 0

    return avg_recall, avg_f1_scores, em



