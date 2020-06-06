from re import compile, IGNORECASE

ADDPIC = compile(r"\A\s*/(add|добавить фото) (\w+) (\w+)\s*\Z", IGNORECASE)
