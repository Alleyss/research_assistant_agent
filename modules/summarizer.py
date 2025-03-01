from transformers import pipeline

def summarize_text(text, max_length=200):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    summary = summarizer(text, max_length=max_length, min_length=50, do_sample=False)
    return summary[0]['summary_text']

# Test
summary = summarize_text(cleaned_text)
print("Summary:", summary)