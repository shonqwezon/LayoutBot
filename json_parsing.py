import json


def process_json(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as infile:
        documents = json.load(infile)

    processed_documents = []

    for doc in documents:
        if not doc.get("Ответ AI (уточнение)", None):
            continue
        processed_doc = {
            "Ответ AI (уточнение)": doc.get("Ответ AI (уточнение)", None),
            "Ресурсы для ответа (уточнение)": doc.get(
                "Ресурсы для ответа (уточнение)", None
            ),
            "Уточненный вопрос пользователя": doc.get(
                "Уточненный вопрос пользователя", None
            ),
        }
        processed_documents.append(processed_doc)
    print("Итого уточнений:", len(processed_documents))
    # Save the new data to the output JSON file
    with open(output_file, "w", encoding="utf-8") as outfile:
        json.dump(processed_documents, outfile, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    input_file = "val_set.json"
    output_file = "val_set_clarify.json"

    process_json(input_file, output_file)
