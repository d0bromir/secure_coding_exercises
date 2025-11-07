```
Задача 2 — Отразен XSS (Flask)
Идея: Приложение връща HTML, съдържащ непречистен потребителски вход.
Уязвимост: render_template_string("<...> %s ..." % q) или некоректен template.
Експлойт: ?q=<script>alert(1)</script> се отразява директно.
Поправка:
    • Рендериране през Jinja шаблон, където авто-escaping е включен (render_template('search.html', q=q)),
    • или пречистване/кодиране на изхода.
Приемни критерии:
    • В vulnerable отговорът съдържа <script>.
    • В fixed <script> липсва / ексейпнат е.
Чести капани:
    • Рендерираш с render_template_string без |e (escape).
    • Създаваш шаблон, но без да подадеш template_folder валидно (на Windows — пътят).
Hints:
    • Hint 1: “Какво прави авто-escaping в Jinja?”
    • Hint 2: “Кое е по-безопасно: render_template или render_template_string?”
    • Hint 3: “Опитай валидна HTML инжекция, после я елиминирай.”
Разширение: Съдържание-безопасни заглавки (CSP), X-Content-Type-Options, X-XSS-Protection (legacy).
```