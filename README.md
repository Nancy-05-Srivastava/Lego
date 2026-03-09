# Agent 2 – Opportunity Discovery Agent

This agent finds hackathons and competitions where a developer's idea can be implemented.

## How it works

1. The user provides a project idea.
2. Azure AI extracts important keywords.
3. The agent searches the internet for hackathons related to those keywords.
4. The opportunities are returned to the master agent.

## Setup

Install dependencies

pip install -r requirements.txt

Set environment variables

AZURE_ENDPOINT=<your endpoint>
AZURE_KEY=<your key>

Run

python hackathon_agent.py
