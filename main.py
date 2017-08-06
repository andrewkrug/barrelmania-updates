from flask import Flask
from flask import render_template
from flask import request

import s3
import sns

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    messages = []
    u = s3.Updates()
    if request.method == 'POST':
        operation = sns.Subscribe(request.form.get('telnumber'))
        operation.subscribe()
        messages = operation.messages

    if u.current() is not None:
        messages.append(u.current())
    return render_template('index.html', messages=messages, updates=u)


if __name__ == '__main__':
    app.run(debug=True)
