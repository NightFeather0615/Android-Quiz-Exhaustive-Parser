import requests
import copy

questionTypes = [
  {
    "index": 0,
    "multipleChoiceSingleAnswer": {
      "answer": {
        "index": -1
      }
    }
  },
  {
    "index": 0,
    "multipleChoiceMultipleAnswer": {
      "answers": []
    }
  },
  {
    "index": 0,
    "matchItems": {
      "answers": []
    }
  },
  {
    "index": 0,
    "fillInTheBlankSingleAnswer": {
      "answer": {
        "answerText": "",
        "index": 0
      }
    }
  }
]

multipleChoiceMultipleAnswerPlaceholder = [
  {"index": 0},
  {"index": 1},
  {"index": 2},
  {"index": 3},
  {"index": 4},
  {"index": 5},
  {"index": 6},
  {"index": 7},
  {"index": 8},
  {"index": 9},
  {"index": 10},
  {"index": 11},
  {"index": 12},
  {"index": 13},
  {"index": 14},
]

payload = {
  "locale": "zh_tw",
  "quiz":{"questions":[]},
  "quizPath": input("Quiz path: ")
}
headers = {
  "Authorization": input("OAuth Token: "),
  "Content-Type": "application/json",
  "Referer": "https://developer.android.com/"
}
url = f"https://content-developerprofiles-pa.googleapis.com/v1/quizzes/{payload['quizPath'].replace('/', '%2F')}/grade?key=AIzaSyAP-jjEJBzmIyKR4F-3XITp8yM9T1gEEI8&alt=json"

response = requests.post(url, data=str(payload), headers=headers)
if response.status_code in [401, 403, 404]:
  print("Unauthorization, invalid authentication credentials or expected OAuth 2 access token")
  exit()

print("Parsing quiz", end="")

index = 0
while True:
  for quizType in questionTypes:
    print(".", end="")
    quiz = copy.deepcopy(quizType)
    quiz["index"] = index

    tempPayload = copy.deepcopy(payload)
    tempPayload["quiz"]["questions"].append(quiz)

    response = requests.post(url, data=str(tempPayload), headers=headers)

    if response.status_code == 200:
      payload = copy.deepcopy(tempPayload)
      index += 1
      break

  if response.status_code == 502:
    print()
    break

print("Exhaustive parsing answers", end="")

tempPayload = copy.deepcopy(payload)

for questionIndex, question in enumerate(tempPayload['quiz']['questions']):
  print(".", end="")

  if not question.get('multipleChoiceSingleAnswer') is None:
    answerIndex = 0
    while True:
      print(".", end="")

      tempPayload = copy.deepcopy(payload)
      tempPayload['quiz']['questions'][questionIndex]['multipleChoiceSingleAnswer']['answer']['index'] = answerIndex

      response = requests.post(url, data=str(tempPayload), headers=headers).json()

      if not response['quiz']['questions'][questionIndex]['multipleChoiceSingleAnswer']['answer'].get('correct') is None:
        payload = copy.deepcopy(tempPayload)
        break

      else:
        answerIndex += 1

  if not question.get('multipleChoiceMultipleAnswer') is None:
    tempPayload = copy.deepcopy(payload)
    tempPayload['quiz']['questions'][questionIndex]['multipleChoiceMultipleAnswer']['answers'] = multipleChoiceMultipleAnswerPlaceholder

    response = requests.post(url, data=str(tempPayload), headers=headers).json()

    tempAnswer = []
    for index, value in enumerate(response['quiz']['questions'][questionIndex]['multipleChoiceMultipleAnswer']['answers']):
      if not value.get('correct') is None:
        print(".", end="")
        tempAnswer.append({"index": index})
    
    tempPayload['quiz']['questions'][questionIndex]['multipleChoiceMultipleAnswer']['answers'] = tempAnswer
    payload = copy.deepcopy(tempPayload)

  if not question.get('matchItems') is None:
    print(".", end="")

  if not question.get('fillInTheBlankSingleAnswer') is None:
    print(".", end="")

response = requests.post(url, data=str(payload), headers=headers).json()

print(f"\nExhaustive parse finished\nScore: {response['quiz'].get('grade', '0')}\nPassed: {response['quiz'].get('passed', 'False')}")

# if not response['quiz'].get('passed') is None:
#   print("Quiz passed, showing answer...")

#   for questionIndex, question in enumerate(tempPayload['quiz']['questions']):
#     if not question.get('multipleChoiceSingleAnswer') is None:
#       print(f"Question {questionIndex}: {question['multipleChoiceSingleAnswer']['answer']['index']}")

#     if not question.get('multipleChoiceMultipleAnswer') is None:
#       print(f"Question {questionIndex}: ", end="")
#       for answer in question['multipleChoiceMultipleAnswer']['answers']:
#         print(answer['index'], end=", ")
#       print("\b")

#     if not question.get('matchItems') is None:
#       print(f"Question {questionIndex}: Unsupport question type, pass")

#     if not question.get('fillInTheBlankSingleAnswer') is None:
#       print(f"Question {questionIndex}: Unsupport question type, pass")
