from textblob import TextBlob

text = "The faculty explains the concepts very clearly and the classes are interesting."
blob = TextBlob(text)

print("Text:", text)
print("Polarity:", blob.sentiment.polarity)
print("Subjectivity:", blob.sentiment.subjectivity)