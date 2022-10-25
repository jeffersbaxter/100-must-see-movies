from tkinter import *
import pandas as pandas

FONT = ("Arial", 21, "italic")

window = Tk()
window.title("100 Must See Movies")
window.config(padx=76, pady=123, width=400, height=647)

listbox = Listbox(window, selectmode=MULTIPLE)
listbox.pack(side=LEFT, fill=BOTH)

scroll = Scrollbar(window, orient="vertical")
scroll.pack(side=RIGHT, fill=BOTH)

movies = []

try:
    movies = pandas.read_csv("movies.csv")
except FileNotFoundError:
    import requests
    from bs4 import BeautifulSoup

    URL = "https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/"

    response = requests.get(URL)

    movie_page = response.text

    soup = BeautifulSoup(movie_page, "html.parser")

    movie_elements = soup.find_all(name="h3", class_="title")

    movies = [movie.getText() for movie in movie_elements]

    movies.reverse()
    seen_list = [False for movie in movies]
    df = pandas.DataFrame({"movie": movies, "seen": seen_list})
    df.to_csv("movies.csv", index=False)
    for movie in movies:
        with open("movies.txt", "a") as movie_file:
            movie_file.write(f"{movie}\n")
finally:
    for index, row in movies.iterrows():
        listbox.insert(END, row["movie"])

    listbox.config(yscrollcommand=scroll.set)
    scroll.config(command=listbox.yview)

window.mainloop()
