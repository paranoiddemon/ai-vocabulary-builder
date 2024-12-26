from typing import Optional
import os
import requests

EUDIC_BASE = "https://api.frdic.com"
ACCESS_KEY: Optional[str] = os.getenv("EUDIC_ACCESS_KEY")
STUDY_LIST_ID: Optional[str] = os.getenv("STUDY_LIST_ID")


class EudicClient:
    """Client for interacting with Eudic API."""

    def __init__(self, access_key: str):
        """Initialize the client with access key."""
        self.access_key = access_key
        self.headers = {
            "Authorization": access_key,
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
        }

    def get_word_note(self, word: str, language: str = "en") -> dict:
        """Get word note from Eudic API.
        
        Args:
            word: The word to look up
            language: Language code, defaults to "en" for English
            
        Returns:
            API response as dict
        """
        response = requests.get(
            f"{EUDIC_BASE}/api/open/v1/studylist/note",
            params={"language": language, "word": word},
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def get_study_list_words(self, list_id: str = STUDY_LIST_ID, language: str = "en") -> dict:
        """Get words from a specific study list."""
        try:
            response = requests.get(
                f"{EUDIC_BASE}/api/open/v1/studylist/words/{list_id}",
                params={"language": language},
                headers=self.headers
            )
            
            response.raise_for_status()
            return response.json()["data"]
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {str(e)}")
            print(f"Response content: {e.response.text if hasattr(e, 'response') else 'No response'}")
            raise

    def add_words_to_study_list(self, words: list[str], list_id: str = STUDY_LIST_ID, language: str = "en") -> dict:
        """Add words to a study list.
        
        Args:
            list_id: The ID of the study list
            words: List of words to add
            language: Language code, defaults to "en" for English
            
        Returns:
            API response as dict
        """
        json={
            "id": list_id,
            "language": language,
            "words": words
        }
        print(json)
        response = requests.post(
            f"{EUDIC_BASE}/api/open/v1/studylist/words",
            params={"language": language},
            headers=self.headers,
            json=json
        )
        print(response.status_code)
        response.raise_for_status()
        print(response.json())
        return response.json()

    def add_word_note(self, word: str, note: str, language: str = "en") -> dict:
        """Add a note to a word.
        
        Args:
            word: The word to add a note to
            note: The note content
            language: Language code, defaults to "en" for English
            
        Returns:
            API response as dict
        """
        response = requests.post(
            f"{EUDIC_BASE}/api/open/v1/studylist/note",
            params={"language": language, "word": word},
            headers=self.headers,
            json={
                "word": word,
                "language": language,
                "note": note
            }
        )
        response.raise_for_status()
        return response.json()

def get_client() -> Optional[EudicClient]:
    """Get an initialized Eudic client if access key is set."""
    if not ACCESS_KEY:
        return None
    if not STUDY_LIST_ID:
        return None
    return EudicClient(ACCESS_KEY)


# client = get_client()
# print(client.get_study_list_words())
# client.add_words_to_study_list(["hello"])
