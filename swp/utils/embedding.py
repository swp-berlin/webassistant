import os

from functools import lru_cache
from typing import List, Iterator

import nltk
import numpy as np

from pdfminer.high_level import extract_text
from fastembed import TextEmbedding
from tokenizers import Encoding

nltk.download('punkt_tab')


def tokenize(text: str, embedding: TextEmbedding) -> Encoding:
    return embedding.model.tokenizer.encode(text)


@lru_cache(maxsize=None)
def get_embedding(model_name):
    return TextEmbedding(
        model_name=model_name,
        local_files_only=True,
        cache_dir='/Users/oliverzander/Projects/SWP/embedding-models',
    )


def prepare_text(text: str):
    return text.replace(f'-{os.linesep}', '')  # remove hyphenation


def get_documents(text: str, embedding: TextEmbedding) -> Iterator[str]:
    """
    Splits the text in documents that are within the embedding's token limit preserving whole sentences when possible.
    """

    sentences = nltk.sent_tokenize(text)
    document = ''

    while sentences:
        sentence, *sentences = sentences

        if document:
            segment = f'{document} {sentence}'
        else:
            segment = sentence

        tokenized = tokenize(segment, embedding)

        if tokenized.overflowing:
            if not document:
                document, sentence = split_sentence(sentence, embedding)
            sentences = [sentence, *sentences]
            yield document
            document = ''
        else:
            document = segment


def split_sentence(sentence: str, embedding: TextEmbedding):
    words = nltk.word_tokenize(sentence)
    chunk = ''

    while words:
        word, *words = words

        if chunk:
            segment = f'{chunk} {word}'
        else:
            segment = word

        tokenized = tokenize(segment, embedding)

        if tokenized.overflowing:
            if not chunk:
                # A word is too long for the token limit (should basically never happen).
                # We have no choice than split it.

                _, end = tokenized.offsets[-2]
                chunk, suffix = word[:end], word[end:]
                words = [suffix, *words]

            return chunk, ' '.join(words)

        chunk = segment


def embed(text: str) -> List[float]:
    text = prepare_text(text)
    embedding = get_embedding('intfloat/multilingual-e5-large')
    documents = [*get_documents(text, embedding)]
    embeddings = [*embedding.embed(documents)]

    return avg(documents, embeddings)


def avg(documents: List[str], embeddings: List[np.array]) -> List[float]:
    """
    Averaging the documents embedding vectors into a single vector using the method described by OpenAI:
    https://cookbook.openai.com/examples/embedding_long_inputs#2-chunking-the-input-text
    """

    weights = [*map(len, documents)]
    average = np.average(embeddings, axis=0, weights=weights)
    average /= np.linalg.norm(average)

    return average.tolist()


def embed_pdf(filepath):
    text = extract_text(filepath)

    return embed(text)


def embed_txt(filepath):
    with open(filepath) as fp:
        text = fp.read()

    return embed(text)


def embed_test():
    return embed_txt('test-data/kurzanalyse6-2021-iab-bamf-soep-befragung-hilfebedarfe.pdfminer.txt')
