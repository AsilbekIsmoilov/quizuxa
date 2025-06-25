import gspread
from oauth2client.service_account import ServiceAccountCredentials
from .models import Question, Answer

def import_questions_from_sheets():
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        'credentials.json',
        ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    )
    client = gspread.authorize(creds)

    sheet = client.open("СВОД").worksheet("тест")
    rows = sheet.get_all_values()

    for row in rows[1:]:
        if not row or not row[0].strip():
            continue  

        question_text = row[0].strip()
        question = Question.objects.create(text=question_text)

        for i in range(1, 5):  
            try:
                answer_text = row[i].strip()
                is_correct = (i == 1)  
                Answer.objects.create(
                    question=question,
                    text=answer_text,
                    is_correct=is_correct
                )
            except IndexError:
                continue  

    print("Импорт завершён")
