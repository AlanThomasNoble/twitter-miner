
    # Alternative Method: Not Working
    '''
    import subprocess
    schema = subprocess.run(
        ['sqlite3', '.open tweets.db','.headers on','.mode csv','.output tweets.csv', '.tables', 'SELECT * FROM tweets;', '.quit' ],
        capture_output=True)

    print(schema)
    table = fileName.strip('.db')
    import os.path

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, fileName)
    p.call(['sqlite3', '.open tweets.db','.headers on',
                '.mode csv','.output tweets.csv', '.tables',
                'SELECT * FROM tweets;', '.quit' ])
    '''