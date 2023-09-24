from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login
import sqlite3
from online_notes_app.db import connection


def reg(request):
    if request.method == "GET":
        return render(request, "registration.html")
    else:
        username = request.POST["username"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        if username is None:
            return HttpResponse("<h3>Введите имя пользователя</h3>")
        elif email is None:
            return HttpResponse("<h3>Введите почту</h3>")
        elif first_name is None:
            return HttpResponse("<h3>Введите полное имя</h3>")
        elif last_name is None:
            return HttpResponse("<h3>Введите полное имя</h3>")
        elif password1 is None or password2 is None:
            return HttpResponse("<h3>Введите пароль</h3>")
        elif password1 != password2:
            return HttpResponse("<h3>Пароли должны совпадать</h3>")
        else:
            sql, db = connection()

        names = sql.execute("SELECT username FROM users").fetchall()
        names = [name[0] for name in names]
        print("Данные из базы 1", names)
        if username not in names:
            sql.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?)", (username, first_name, last_name, email, password1))
            db.commit()

        names = sql.execute("SELECT * FROM users").fetchall()
        print("Данные из базы после добавления нового Юзера", names)

        return render(request, "add_note.html")


def logining(request):
    if request.method == "GET":
        return render(request, "authorization.html")
    else:
        data = request.POST
        try:
            sql, db = connection()
            username = data['username']
            password = data['password']
            auth_user = sql.execute(f'SELECT password FROM users WHERE username="{username}"').fetchall()
            if password == auth_user[0][0]:
                request.session[f"{username}"] = username
                response = HttpResponse(f"<h3>Вы, {username}, успешно авторизованы</h3>")
                response.set_cookie("username", username)
                return response
        except KeyError:
            return HttpResponse("<h3>Заполните все поля</h3>")


def logout(request):
    username = request.COOKIES["username"]
    del request.session[f"{username}"]
    return redirect(logining)


def notes(request):
    sql, db = connection()
    username = request.COOKIES["username"]

    author_notes = sql.execute(f"SELECT note FROM notes WHERE author = ?", (username,)).fetchall()
    print(author_notes)
    return render(request, "notes.html", {"notes": author_notes})


def add_note(request):
    if request.method == "GET":
        return render(request, "add_note.html")
    else:
        sql, db = connection()
        username = request.COOKIES["username"]
        note = request.POST["note-text"]
        sql.execute("INSERT INTO notes (note, author) VALUES (?, ?)", (note, username))
        db.commit()
        return render(request, "add_note.html")

