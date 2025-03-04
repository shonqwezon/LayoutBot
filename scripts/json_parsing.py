import json


def process_json(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as infile:
        documents = json.load(infile)

    processed_documents = []

    ai_answer = "Ответ AI (уточнение)"
    resourses = "Ресурсы для ответа (уточнение)"
    question = "Уточненный вопрос пользователя"

    for doc in documents:
        if not doc.get(question, None):
            continue
        processed_doc = {
            ai_answer: doc.get(ai_answer, None),
            resourses: doc.get(resourses, None),
            question: doc.get(question, None),
        }
        processed_documents.append(processed_doc)
    print("Итого уточнений:", len(processed_documents))
    # Save the new data to the output JSON file
    with open(output_file, "w", encoding="utf-8") as outfile:
        json.dump(processed_documents, outfile, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    base_name = "train_set"
    input_file = f"data/{base_name}.json"
    output_file = f"data/{base_name}_clarify.json"
    process_json(input_file, output_file)
