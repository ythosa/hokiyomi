from re import compile, IGNORECASE

ECHO = compile(r"\A\s*/(echo|эхо)\s*\Z", IGNORECASE)
ADDPIC = compile(r"\A\s*/(addpic|добавить фото)\s*\Z", IGNORECASE)