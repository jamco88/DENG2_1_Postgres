import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    '''
    Adds song and artist entries to their respective tables in the database.
    
        Parameters:
            cur (obj): a psycopg2 cursor object
            filepath (str): the path to the raw song data
            
        Returns:
            None
    '''
    df = pd.read_json(filepath, lines=True)

    song_data = list(df[["song_id", "title", "artist_id", "year", "duration"]].values[0])
    cur.execute(song_table_insert, song_data)
    
    artist_data = list(df[["artist_id", "artist_name", "artist_location", "artist_latitude", "artist_longitude"]].values[0])
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    '''
    Processes raw log data file, adds time and user entries to their respective tables in the database. Adds Songplay entries to a new table.
    
        Parameters:
            cur (obj): a psycopg2 cursor object
            filepath (str): the path to the raw log data
            
        Returns:
            None
    '''   
    

    df = pd.read_json(filepath, lines=True)

    df = df.loc[df.page == 'NextSong']

    t = pd.to_datetime(df.ts, unit='ms')
    
    time_data = [df.ts.values, t.dt.hour.values, t.dt.day.values,
                 t.dt.weekofyear.values, t.dt.month.values, t.dt.year.values,
                 t.dt.weekday.values]
    column_labels = ['timestamp', 'hour', 'day', 'week', 'month', 'year', 'weekday']
    time_df = pd.DataFrame(dict(zip(column_labels, time_data)))

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    user_df = df[["userId", "firstName", "lastName","gender","level"]]

    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    for index, row in df.iterrows():
        
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        songplay_data = [row.ts, row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent]
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    '''
    Higher level function that applies each processing function to the data.
    
        Parameters:
            cur (obj): a psycopg2 cursor object
            conn (obj): psycopg2 connection object
            filepath (str): the path to the raw data
            func(func): a file processing function
            
        Returns:
            None
    ''' 
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()
    print("job's a good'un")