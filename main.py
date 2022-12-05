import requests
import copy
import time

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

headers = {
  "Authorization": input("OAuth Token: "),
  "Content-Type": "application/json",
  "Referer": "https://developer.android.com/"
}
payload = {
  "locale": "zh_tw",
  "quiz":{"questions":[]},
  "quizPath": input("Quiz path: ")
}
url = f"https://content-developerprofiles-pa.googleapis.com/v1/quizzes/{payload['quizPath'].replace('/', '%2F')}/grade?key=AIzaSyAP-jjEJBzmIyKR4F-3XITp8yM9T1gEEI8&alt=json"

response = requests.post(url, data=str(payload), headers=headers)
if response.status_code in [401, 403, 404]:
  print("Unauthorization, invalid authentication credentials or expected OAuth 2 access token")
  exit()

print("""
0: multipleChoiceSingleAnswer
1: multipleChoiceMultipleAnswer
2: matchItems
3: fillInTheBlankSingleAnswer
""")
quizTypeData = [int(i) for i in input("Please enter quiz type for each questions (e.g. 12331023): ")]

for index, quizTypeIndex in enumerate(quizTypeData):
  quiz = copy.deepcopy(questionTypes[quizTypeIndex])
  quiz["index"] = index
  tempPayload = copy.deepcopy(payload)
  tempPayload["quiz"]["questions"].append(quiz)
  payload = copy.deepcopy(tempPayload)

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

      if response['quiz']['questions'][questionIndex].get('correct') is True:
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
      if value.get('correct') is True:
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
print(f"Check the website down below to earn the badge\nhttps://developer.android.com/courses/pathways/{payload['quizPath'].split('/')[-1]}")