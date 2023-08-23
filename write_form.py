from __future__ import print_function

from googleapiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools

def create_write_form(games: dict, week: int, final: str):
    SCOPES = "https://www.googleapis.com/auth/forms.body"
    DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"

    store = file.Storage('misc/token.json')
    creds = None
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('misc/forms_secret.json', SCOPES)
        creds = tools.run_flow(flow, store)

    form_service = discovery.build('forms', 'v1', http=creds.authorize(
        Http()), discoveryServiceUrl=DISCOVERY_DOC, static_discovery=False)

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