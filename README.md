# hackaton

Проект по кейсу "Оценка профессиональных компетенций"

Для запуска контейнера прописать в терминале в корне: docker compose up.
Перед пользованием backend нужно скачать всё из requirements.txt: pip install -r "requirements.txt"
Для запуска бэка в корне прописать в терминале в корне: uvicorn app.main:app --reload --port 8080

Потом подумаю о том, чтобы бэк сам поднимался отдельным образом, общаясь через порты.
