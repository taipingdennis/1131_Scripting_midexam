import lib

# 執行選單
def main(conn, cursor):
    while True:
        print("\n")
        print("----- 電影管理系統 -----")
        print("1. 匯入電影資料檔")
        print("2. 查詢電影")
        print("3. 新增電影")
        print("4. 修改電影")
        print("5. 刪除電影")
        print("6. 匯出電影")
        print("7. 離開系統")
        print("------------------------")

        option = input("請選擇操作選項 (1-7): ")

        if option == '7':
            print("系統已退出。")
            break
        elif option == '1':
            lib.import_movies(conn, cursor, JSON_IN_PATH)
        elif option == '2':
            lib.search_movies(cursor)
        elif option == '3':
            lib.add_movie(conn, cursor)
        elif option == '4':
            lib.modify_movie(conn, cursor)
        elif option == '5':
            lib.delete_movies(conn, cursor)
        elif option == '6':
            lib.export_movies(cursor, JSON_OUT_PATH)
        else:
            print("請輸入正確的選項")

# 主程式
DB_PATH = 'movie.db'
JSON_IN_PATH = 'movies.json'
JSON_OUT_PATH = 'exported.json'

with lib.connect_db(DB_PATH) as conn:
    # sqlite3.Cursor 物件不支援 with 語法
    cursor = conn.cursor()
    try:
        lib.create_table(cursor)
        main(conn, cursor)
    finally:
        cursor.close()
