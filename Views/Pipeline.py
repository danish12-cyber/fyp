import csv
import time
from newspaper import Article
import nltk
import spacy
import re
from collections import defaultdict

# Load the spaCy English model
nlp = spacy.load('en_core_web_sm')

# Define list of news article URLs
urls = [
    'https://www.dawn.com/news/1878485/kp-to-launch-polio-drive-on-dec-16-amid-challenges',
    'https://www.dawn.com/news/1878521/senate-unanimously-passes-national-forensic-agency-bill-2024',
    'https://www.dawn.com/news/1878176/kp-govt-forms-working-group-for-climate-change-initiative',
    'https://www.dawn.com/news/1878326/amid-ongoing-digital-law-reforms-govt-proposes-new-central-cybercrime-forensics-agency',
]

# Define trigger words for event extraction
trigger_words = [
    'announced', 'passed', 'introduced', 'unveiled', 'declared', 'debated', 'discussed', 'hearing',
    'reviewed', 'rejected', 'voted', 'implemented', 'enforced', 'issued', 'ruled', 'guideline',
    'regulation', 'challenged', 'appealed', 'protested', 'supported', 'poll', 'report', 'study',
    'signed', 'agreed', 'treaty', 'consultation', 'emergency', 'imposed', 'urgent', 'order', 'plan',
    'imposed', 'sit-in', 'striked', 'okayed', 'Formed', 'rallies'
]

# Compile the trigger words into a regular expression pattern for easier matching
trigger_pattern = re.compile(r'\b(?:' + '|'.join(trigger_words) + r')\b', re.IGNORECASE)

# Limit the number of sentences in the event description
# MAX_EVENT_SENTENCES = 2

# Helper function to extract arguments using dependency parsing
def extract_arguments(doc):
    arguments = {
        "Actor": [],
        "Action": [],
        "Target": [],
        "Location": [],
        "Time": []
    }

    for token in doc:
        if token.dep_ in ("nsubj", "nsubjpass") and token.ent_type_ in ("PERSON", "ORG", "GPE"):
            arguments["Actor"].append(token.text)
        if token.pos_ == "VERB" and trigger_pattern.search(token.text):
            arguments["Action"].append(token.lemma_)
        if token.dep_ == "dobj":
            arguments["Target"].append(token.text)
        if token.ent_type_ in ("GPE", "LOC"):
            arguments["Location"].append(token.text)
        if token.ent_type_ in ("DATE", "TIME"):
            arguments["Time"].append(token.text)

    for key in arguments:
        arguments[key] = list(set(arguments[key]))

    return arguments

# Function to perform sentence tokenization using spaCy
def custom_sent_tokenize_spacy(text):
    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]
    return sentences

def event_extract(url, MAX_EVENT_SENTENCES):
    # Create a CSV file to store the dataset
    with open('enhanced_event_dataset.csv', mode='w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Event Type", "Event Description", "Arguments", "Entities", "Publish Date", "URL"])

        
        article = Article(url)
        article.download()
        article.parse()

        sentences = custom_sent_tokenize_spacy(article.text)

        event_sentences = [sentence for sentence in sentences if trigger_pattern.search(sentence)]
        event_description = ' '.join(event_sentences[:MAX_EVENT_SENTENCES]) if event_sentences else 'No specific event mentioned'

        event_triggers = [word for word in article.text.lower().split() if word in trigger_words]
        event_type = ', '.join(set(event_triggers)) if event_triggers else 'None'

        doc = nlp(article.text)
        entities = [(ent.text, ent.label_) for ent in doc.ents]

        arguments = extract_arguments(doc)

        publish_date = article.publish_date
        if not publish_date:
            date_entities = [ent.text for ent in doc.ents if ent.label_ == "DATE"]
            publish_date = date_entities[0] if date_entities else "Unknown"

        print(f"Event Type: {event_type}")
        print(f"Event Description: {event_description}")
        print(f"Publishing Date: {publish_date}")
        print("-" * 50)

        writer.writerow([
            article.title,
            event_type,
            event_description,
            arguments,
            entities,
            publish_date,
            article.url
        ])

        time.sleep(2)
    return event_type
    print("Enhanced dataset collection complete. Data saved to 'enhanced_event_dataset.csv'.")
