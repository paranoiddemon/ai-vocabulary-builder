from typing import Optional
import httpx

EUDIC_BASE = "https://api.frdic.com"
ACCESS_KEY: Optional[str] = None

class EudicClient:
    """Client for interacting with Eudic API."""

    def __init__(self, access_key: str):
        """Initialize the client with access key."""
        self.access_key = access_key
        self.headers = {
            "Authorization": f"{access_key}",
            "Host": "api.frdic.com"
        }

    async def get_word_note(self, word: str, language: str = "en") -> dict:
        """Get word note from Eudic API.
        
        Args:
            word: The word to look up
            language: Language code, defaults to "en" for English
            
        Returns:
            API response as dict
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{EUDIC_BASE}/api/open/v1/studylist/note",
                params={"language": language, "word": word},
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()

    async def get_study_list_words(self, list_id: str, word: str, language: str = "en") -> dict:
        """Get words from a specific study list.
        
        Args:
            list_id: The ID of the study list
            word: The word to look up
            language: Language code, defaults to "en" for English
            
        Returns:
            API response as dict
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{EUDIC_BASE}/api/open/v1/studylist/words/{list_id}",
                params={"language": language, "word": word},
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()

    async def add_words_to_study_list(self, list_id: str, words: list[str], language: str = "en") -> dict:
        """Add words to a study list.
        
        Args:
            list_id: The ID of the study list
            words: List of words to add
            language: Language code, defaults to "en" for English
            
        Returns:
            API response as dict
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{EUDIC_BASE}/api/open/v1/studylist/words",
                params={"language": language},
                headers=self.headers,
                json={
                    "id": list_id,
                    "language": language,
                    "words": words
                }
            )
            response.raise_for_status()
            return response.json()

    async def add_word_note(self, word: str, note: str, language: str = "en") -> dict:
        """Add a note to a word.
        
        Args:
            word: The word to add a note to
            note: The note content
            language: Language code, defaults to "en" for English
            
        Returns:
            API response as dict
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
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

def set_access_key(key: str):
    """Set the global access key for Eudic API."""
    global ACCESS_KEY
    ACCESS_KEY = key

def get_client() -> Optional[EudicClient]:
    """Get an initialized Eudic client if access key is set."""
    if not ACCESS_KEY:
        return None
    return EudicClient(ACCESS_KEY)