import psycopg2

<<<<<<< HEAD
def get_db():
    return psycopg2.connect(host="localhost", dbname="authme", user="chief", password="tacosgood")

def get_db_instance():
    db = get_db()
    cur = db.cursor()
    return db, cur
=======

def get_db():
    return psycopg2.connect(host="localhost", dbname="authme" , user="loki", password="4prez")

def get_db_instance():  
    db  = get_db()
    cur  = db.cursor( )

    return db, cur 



if __name__ == "__main__":
    db, cur = get_db_instance()

    cur.execute("select * from users")
    for r in cur.fetchall():
        print(r)

    cur.execute("create table music ( song_name varchar(255), rating int);")
    db.commit()




>>>>>>> f1b88be3653e3b5dcf2d6045c81bf72789682485
