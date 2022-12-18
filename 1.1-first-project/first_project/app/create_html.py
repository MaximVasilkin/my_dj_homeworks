def create_html(code):
    html = '''
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>Title</title>
    </head>
    <body>
        {}
        </br>
        <strong><a href="/">На главную</a></strong>
    </body>
    </html>
    '''.format(code)
    return html