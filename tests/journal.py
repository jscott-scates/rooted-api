import json
import datetime
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rootedapi.models import Sage, Spread, Deck, DeckType

class JournalTests(APITestCase):
    def setUp(self) -> None:
        """Register a New User, assign deck, create spread"""

        """Create DeckType to Assign to Deck"""
        self.deck_type = DeckType.objects.create(
            name="oracle", 
            label="Oracle", 
            description='Rooted messages from the earth.'
        )
        self.assertEqual(DeckType.objects.count(), 1)
        
        """Create Deck to Assign to Sage"""
        self.deck = Deck.objects.create(
            id=1, 
            name="The Rooted Deck",
            deck_type=self.deck_type
        )
        self.assertEqual(Deck.objects.count(), 1)

        #Register New User
        url ="/register"
        data = {
            "username": "steve",
            "password": "Admin8*",
            "email": "steve@stevebrownlee.com",
            "first_name": "Steve",
            "last_name": "Brownlee",
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        json_response = json.loads(response.content)
        self.token = json_response["token"]

        #Get Created Sage
        self.user = User.objects.get(username="steve")
        self.sage = Sage.objects.get(user = self.user)
        self.assertEqual(self.sage.deck,self.deck)

        #Create and assign a deck to the sage
        self.sage.deck = self.deck
        self.sage.save()

        #Create a spread 
        self.spread = Spread.objects.create(
            name="Daily Draw",
            description = "Draw a card on the daily",
            num_positions = 1)       
        self.assertEqual(Spread.objects.count(),1)

    
    def test_create_new_journal(self):
        """Ensure that we can create a new entry, 
        does not need to contain a title, content, mood, or lunar phase upon instantiation. 
        """

        url="/journal-entries"
        data = {
            "spread":1
        }

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        response = self.client.post(url, data, format="json")
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json_response["spread"]["id"],1)

    def test_delete_a_journal(self):
        """Ensure that we can delete an existing journal entry"""

        #Create 3 journal entries
        self.test_create_new_journal()
        self.test_create_new_journal()
        self.test_create_new_journal()

        #Authenticate the Current User
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)

        #Get all entries to find the correct ID to delete
        response = self.client.get("/journal-entries", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        entries = json.loads(response.content)
        self.assertEqual(len(entries), 3)

        entry_id = entries[0]["id"]
        url = f"/journal-entries/{entry_id}"

        #Delete id 1 journal entry
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        #Get deleted journal entry, make sure it was not found
        response = self.client.get(url, None, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        #Get list of all journal entries, make sure there are only 2
        response = self.client.get("/journal-entries", format="json")
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json_response),2)

