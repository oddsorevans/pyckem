from __future__ import print_function

import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def create_write_form(games: dict, week: int, final: str):
    SCOPES = ['https://www.googleapis.com/auth/forms.body']
    DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"

    creds = None
    token_path = 'misc/token.json'
    credentials_path = 'misc/forms_secret.json'

    # Load credentials from environment variable (for GitHub Actions) or file
    if os.environ.get('GOOGLE_CREDENTIALS_JSON'):
        creds_data = json.loads(os.environ.get('GOOGLE_CREDENTIALS_JSON'))
        creds = Credentials.from_authorized_user_info(creds_data, SCOPES)
    elif os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    # If there are no valid credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"Error refreshing token: {e}")
                creds = None

        if not creds:
            if not os.path.exists(credentials_path):
                raise FileNotFoundError(f"Credentials file not found: {credentials_path}")
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    form_service = build('forms', 'v1', credentials=creds,
                        discoveryServiceUrl=DISCOVERY_DOC, static_discovery=False)

    # Request body for creating a form
    NEW_FORM = {
        "info": {
            "title": f"Pickem Week {week}",
        }
    }

    # Creates the initial form
    result = form_service.forms().create(body=NEW_FORM).execute()

    ASK_NAME = {
        "requests": [{
            "createItem": {
                "item": {
                    "title": "What is your name?",
                    "questionItem": {
                        "question": {
                            "required": True,
                            "textQuestion": {
                                "paragraph":False
                            }
                        }
                    },
                },
                "location": {
                    "index": 0
                }
            }
        }]
    }
    # Adds the question to the form
    question_setting = form_service.forms().batchUpdate(formId=result["formId"], body=ASK_NAME).execute()

    index = 1
    for key, value in games.items():
        # Request body to add a multiple-choice question
        NEW_QUESTION = {
            "requests": [{
                "createItem": {
                    "item": {
                        "title": key,
                        "questionItem": {
                            "question": {
                                "required": True,
                                "choiceQuestion": {
                                    "type": "RADIO",
                                    "options": [
                                        {"value": value['home']},
                                        {"value": value['away']}
                                    ],
                                    "shuffle": False
                                }
                            }
                        },
                    },
                    "location": {
                        "index": index
                    }
                }
            }]
        }
        # Adds the question to the form
        question_setting = form_service.forms().batchUpdate(formId=result["formId"], body=NEW_QUESTION).execute()
        index += 1


    ASK_FINAL = {
        "requests": [{
            "createItem": {
                "item": {
                    "title": f"Tiebreaker, {final}",
                    "questionItem": {
                        "question": {
                            "required": True,
                            "textQuestion": {
                                "paragraph":False
                            }
                        }
                    },
                },
                "location": {
                    "index": index
                }
            }
        }]
    }
    # Adds the question to the form
    question_setting = form_service.forms().batchUpdate(formId=result["formId"], body=ASK_FINAL).execute()
    # Prints the result to show the question has been added
    get_result = form_service.forms().get(formId=result["formId"]).execute()
    print(get_result)   