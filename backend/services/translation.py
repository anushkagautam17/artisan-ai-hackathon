import os
from typing import List

def translate_texts(texts: List[str], target_language: str) -> List[str]:
    """
    Uses Google Cloud Translate v3 to translate a batch of strings.
    """
    from google.cloud import translate_v3 as translate

    client = translate.TranslationServiceClient()

    project_id = os.getenv("VERTEX_PROJECT_ID")
    location = os.getenv("VERTEX_LOCATION", "us-central1")
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        contents=texts,
        target_language_code=target_language,
        parent=parent,
        mime_type="text/plain",
    )
    return [t.translated_text for t in response.translations]
