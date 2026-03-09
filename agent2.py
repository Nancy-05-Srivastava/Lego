import requests
from ddgs import DDGS

import os

endpoint = os.getenv("AZURE_ENDPOINT")
key = os.getenv("AZURE_KEY")

def extract_keywords(text):

    url = endpoint + "/language/:analyze-text?api-version=2023-04-01"

    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json"
    }

    data = {
      "kind": "KeyPhraseExtraction",
      "analysisInput": {
        "documents": [
          {
            "id": "1",
            "language": "en",
            "text": text
          }
        ]
      }
    }

    response = requests.post(url, headers=headers, json=data)

    result = response.json()

    return result["results"]["documents"][0]["keyPhrases"]


def find_opportunities(idea):

    keywords = extract_keywords(idea)

    results = []

    with DDGS() as ddgs:

        for keyword in keywords:

            query = f"{keyword} hackathon"

            search_results = ddgs.text(query, max_results=5)

            for r in search_results:

                results.append({
                    "keyword": keyword,
                    "title": r["title"],
                    "link": r["href"]
                })

    return {
        "idea": idea,
        "keywords": keywords,
        "opportunities": results
    }
