import json
import string

with open('jsons/fastmenace.json') as f:
  data = json.load(f)

split_by_sender = False

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

freq = {}
sender_freqs = {}

for message_data in data['messages']:
    if 'content' in message_data:
        sender = message_data['sender_name']
        if (sender not in sender_freqs):
            sender_freqs[sender] = {}
        msg = message_data['content']
        words = msg.split()
        for word in words:
            word = word.translate(str.maketrans('', '', string.punctuation))
            cleaned_word = word.lower()
            if (len(word) > 0):
                if split_by_sender:
                    if (cleaned_word not in sender_freqs[sender]):
                        sender_freqs[sender][cleaned_word] = 0
                    sender_freqs[sender][cleaned_word] += 1
                else:
                    if (cleaned_word not in freq):
                        freq[cleaned_word] = 0
                    freq[cleaned_word] += 1
    else:
        pass

def without_stopwords(freq, quant):
    sort_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    count = 0
    for tup in sort_freq:
        if (count == quant):
            break
        if (tup[0] not in stop_words):
            print(count, tup[0])
            count += 1

for sender in sender_freqs:
    print(sender)
    without_stopwords(sender_freqs[sender], 30)

without_stopwords(freq, 30)