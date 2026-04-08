import csv
import uuid

class ImportService:

    def __init__(self):
        self.batches = {}
        self.rules = {
            "name": {"required": True},
            "description": {"required": True, "max_words": 30},
            "category": {"required": True},
            "city": {"required": True},
            "address": {"required": True,}
        }

    async def process_file(self, file):
        content = await file.read()
        lines = content.decode("utf-8").splitlines()
        reader = csv.DictReader(lines)

        batch_id = str(uuid.uuid4())
        errors = []
        valid = 0

        for i, row in enumerate(reader):
            row_errors = self.validate_row(row, i)

            if row_errors:
                errors.extend(row_errors)
            else:
                valid += 1

        self.batches[batch_id] = {
            "total": len(lines),
            "valid": valid,
            "errors": errors
        }

        return {
            "batch_id": batch_id,
            "valid_rows": valid,
            "errors": len(errors)
        }

    def validate_row(self, row, index):
        errors = []

        for field, rule in self.rules.items():
            value = row.get(field)

            if rule.get("required") and not value:
                errors.append({
                    "row": index,
                    "field": field,
                    "error": "Campo requerido vacío"
                })
        
            if "max_words" in rule and value:
                word_count = len(value.split())
                if word_count > rule["max_words"]:
                    errors.append({
                        "row": index,
                        "field": field,
                        "error": f"Máximo {rule['max_words']} palabras"
                    })
        return errors
