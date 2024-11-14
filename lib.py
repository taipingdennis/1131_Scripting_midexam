import sqlite3
import json

'''連線資料庫'''
def connect_db(DB):
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row  # 使查詢結果可以用欄位名稱來存取
    return conn

'''建立資料表'''
def create_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS "movies" (
            "id" INTEGER PRIMARY KEY AUTOINCREMENT,
            "title" TEXT NOT NULL,
            "director" TEXT NOT NULL,
            "genre" TEXT NOT NULL,
            "year" INTEGER NOT NULL,
            "rating" REAL CHECK(rating >= 1.0 AND rating <= 10.0)
        );
    ''')

'''列出電影紀錄'''
def list_rpt(data):
    print()
    print(f"{'電影名稱':{chr(12288)}<8}{'導演':{chr(12288)}<12}{'類型':{chr(12288)}<5}{'上映年份':{chr(12288)}<5}{'評分':{chr(12288)}^5}")
    print("------------------------------------------------------------------------")
    for record in data:
        print(f"{record['title']:{chr(12288)}<8}{record['director']:{chr(12288)}<12}{record['genre']:{chr(12288)}<5}{record['year']:{chr(12288)}<5}{record['rating']:{chr(12288)}>6}")

'''查詢特定電影'''
def specific_movie_rpt(cursor, movie_title) -> list:
    try:
        cursor.execute("SELECT * FROM movies WHERE title LIKE ?", (f'%{movie_title}%',))
        data = cursor.fetchall()
    except sqlite3.Error as error:
        print(f"執行 SELECT 操作時發生錯誤：{error}")
        return []

    if data:
        list_rpt(data)
    else:
        print("查無資料")
    return data

'''1. 匯入電影資料'''
def import_movies(conn, cursor, json_in_path):
    with open(json_in_path, 'r', encoding='utf-8') as file:
        movies = json.load(file)

    for movie in movies:
        cursor.execute('''
            INSERT INTO movies (title, director, genre, year, rating)
            VALUES (?, ?, ?, ?, ?)
        ''', (movie['title'], movie['director'], movie['genre'], movie['year'], movie['rating']))
    conn.commit()
    print("電影已匯入。")

'''2. 查詢電影'''
def search_movies(cursor):
    option = input("查詢全部電影嗎？(y/n): ")
    cursor.execute("SELECT * FROM movies")
    data = cursor.fetchall()

    if len(data) == 0:
        print("查無資料")
        return

    if option == 'y':
        # 查詢全部電影
        list_rpt(data)
    elif option == 'n':
        # 查詢指定電影
        movie_title = input("請輸入電影名稱: ")
        specific_movie_rpt(cursor, movie_title)
    else:
        print("輸入格式錯誤, 無法執行查詢")

'''3. 新增電影'''
def add_movie(conn, cursor):
    title = input("電影名稱: ")
    director = input("導演: ")
    genre = input("類型: ")
    year = input("上映年份: ")
    rating = input("評分 (1.0 - 10.0): ")

    cursor.execute('''
        INSERT INTO movies (title, director, genre, year, rating)
        VALUES (?, ?, ?, ?, ?)
    ''', (title, director, genre, year, rating))

    conn.commit()
    print("電影已新增。")

'''4. 修改電影'''
def modify_movie(conn, cursor):
    movie_title = input("請輸入要修改的電影名稱: ")
    data = specific_movie_rpt(cursor, movie_title)

    record = data[0]
    print()
    new_title = input("請輸入新的電影名稱 (若不修改請直接按 Enter): ") or record["title"]
    new_director = input("請輸入新的導演 (若不修改請直接按 Enter): ") or record["director"]
    new_genre = input("請輸入新的類型 (若不修改請直接按 Enter): ") or record["genre"]
    new_year = input("請輸入新的上映年份 (若不修改請直接按 Enter): ") or record["year"]
    new_rating = input("請輸入新的評分 (1.0 - 10.0) (若不修改請直接按 Enter): ") or record["rating"]

    cursor.execute('''
        UPDATE movies
        SET title = ?, director = ?, genre = ?, year = ?, rating = ?
        WHERE id = ?;
    ''', (new_title, new_director, new_genre, new_year, new_rating, record["id"]))

    conn.commit()
    print("資料已修改")

'''5. 刪除電影'''
def delete_movies(conn, cursor):
    option = input("刪除全部電影嗎？(y/n): ")

    if option == 'y':
        # 刪除全部電影
        cursor.execute("DELETE FROM movies")

    elif option == 'n':
        # 刪除指定電影
        movie_title = input("請輸入要刪除的電影名稱: ")
        specific_movie_rpt(cursor, movie_title)
        confirm = input("是否要刪除(y/n): ")
        if confirm == 'y':
            cursor.execute("DELETE FROM movies WHERE title LIKE ?", (f'%{movie_title}%',))
            print("電影已刪除。")

    else:
        print("輸入格式錯誤, 無法執行刪除")

    conn.commit()

'''6. 匯出電影資料'''
def export_movies(cursor, json_out_path):
    option = input("匯出全部電影嗎？(y/n): ")

    if option == 'y':
        cursor.execute("SELECT * FROM movies")
    elif option == 'n':
        movie_title = input("請輸入要匯出的電影名稱: ")
        cursor.execute("SELECT * FROM movies WHERE title LIKE ?", (f'%{movie_title}%',))

    data = cursor.fetchall()

    # 匯出到json檔
    movies_list = [dict(record) for record in data]
    with open(json_out_path, 'w', encoding='utf-8') as file:
        json.dump(movies_list, file, ensure_ascii = False, indent = 4)
    print(f"電影資料已匯出至 {json_out_path}")
