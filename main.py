import json
import string
import os

stop_words = ["a", "able", "about", "across", "after", "all", "almost", "also", "am", "among", "an",
            "and", "any", "are", "as", "at", "be", "because", "been", "but", "by", "can", "cannot",
            "could", "did", "do", "does", "either", "else", "ever", "every", "for", "from", "get",
            "got", "had", "has", "have", "he", "her", "hers", "him", "his", "how", "however", "i",
            "if", "in", "into", "is", "it", "its", "just", "least", "let", "like", "likely", "may",
            "me", "might", "most", "must", "my", "neither", "no", "nor", "not", "of", "off", "often",
            "on", "only", "or", "other", "our", "own", "rather", "said", "say", "says", "she", "should",
            "since", "so", "some", "than", "that", "the", "their", "them", "then", "there", "these",
            "they", "this", "tis", "to", "too", "twas", "us", "wants", "was", "we", "were", "what",
            "when", "where", "which", "while", "who", "whom", "why", "will", "with", "would", "yet",
            "you", "your"]

class Parser:
    freq = {}
    sender_freqs = {}
    message_count = {}
    message_length = {}

    def __init__(self):
        pass

    def load_file(self, file_name):
        with open(file_name) as f:
            data = json.load(f)
            self.add_data(data)

    def load_folder(self, folder_name):
        for file in os.listdir("./" + folder_name):
            if file.endswith(".json"):
                self.load_file(os.path.join("./", folder_name, file))

    def add_data(self, data):
        for participant in data['participants']:
            participant_name = participant['name']
            if participant_name not in self.sender_freqs:
                self.sender_freqs[participant_name] = {}
                self.message_count[participant_name] = 0
                self.message_length[participant_name] = 0
                
        for message_data in data['messages']:
            if 'content' in message_data:
                sender = message_data['sender_name']
                msg = message_data['content']
                self.message_count[sender] += 1
                self.message_length[sender] += len(msg)

                msg = msg.replace("\u00e2\u0080\u0099", "'")

                words = msg.split()
                for word in words:
                    word = word.translate(str.maketrans('', '', string.punctuation))
                    cleaned_word = word.lower()
                    if (len(word) > 1):
                        if (cleaned_word not in self.sender_freqs[sender]):
                            self.sender_freqs[sender][cleaned_word] = 0
                        self.sender_freqs[sender][cleaned_word] += 1
                        if (cleaned_word not in self.freq):
                            self.freq[cleaned_word] = 0
                        self.freq[cleaned_word] += 1
            else:
                pass

    def uniqueness(self, cutoff=50):
        weight_words = []
        for x in self.freq:
            if (self.freq[x] < cutoff):
                continue
            total_weight = 0
            max_weight = 0
            max_sender = None
            for sender in self.sender_freqs:
                if (x in self.sender_freqs[sender]):
                    normalized = 10000 * self.sender_freqs[sender][x] / self.message_length[sender]
                    total_weight += normalized
                    if (normalized > max_weight):
                        max_weight = normalized
                        max_sender = sender
            weight_words.append((x, max_weight / total_weight, max_sender))

        sorted_weights = sorted(weight_words, key = lambda x: x[1], reverse=True)
        
        unique_by_person = {}
        for sender in self.sender_freqs:
            unique_by_person[sender] = []
        for tup in sorted_weights:
            if (len(unique_by_person[tup[2]]) < 10):
                unique_by_person[tup[2]].append((tup[0], tup[1]))

        for person in unique_by_person:
            print(person)
            for i in range(0, len(unique_by_person[person])):
                print("{}. {} ({:.3f})".format(i, unique_by_person[person][i][0], unique_by_person[person][i][1]))

    def message_lengths(self):
        # TODO: sort this
        # print(self.message_count)
        # print(self.message_length)

        for sender in self.sender_freqs:
            if (parser.message_count[sender] > 0):
                print ("{}: {}".format(sender, parser.message_length[sender] / self.message_count[sender]))
        
    def basic_freq(self, all_num = 20, indiv_num = 10):
        print("Overall Frequency")
        without_stopwords(self.freq, all_num)
        for sender in parser.sender_freqs:
            print(sender)
            without_stopwords(parser.sender_freqs[sender], indiv_num)


def without_stopwords(freq, quant):
    sort_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    count = 0
    for tup in sort_freq:
        if (count == quant):
            break
        if (tup[0] not in stop_words):
            print(count, tup[0])
            count += 1

parser = Parser()
# parser.load_file("jsons/message_1.json")
parser.load_folder("jsons/someone")

# Printing
parser.basic_freq(indiv_num=10)
parser.message_lengths()
parser.uniqueness(cutoff=50)

# additional information loop
while (True):
    x = input()
    if (x in parser.freq):
        print("total", parser.freq[x])
        total_weight = 0
        max_weight = 0
        for sender in parser.sender_freqs:
            if (x in parser.sender_freqs[sender]):
                normalized = 10000 * parser.sender_freqs[sender][x] / parser.message_length[sender]
                total_weight += normalized
                max_weight = max(max_weight, normalized)
                print(sender, normalized)
        print(max_weight / total_weight)
    else:
        print("NONE")