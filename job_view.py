from flask import Flask, render_template
app = Flask(__name__)
from sqlalchemy import *


@app.route('/')
def index():
    
    #highlight = {'min': 40, 'max': 80, 'rain': 5}
    return render_template('index.html')

@app.route('/jobs/')
def jobs_landing():
    return render_template('jobs.html')


@app.route('/job/<post_id>')
def job_post(post_id):
    db = create_engine("mysql+mysqldb://root@127.0.0.1/craigs")
    connection = db.connect()
    temp_query = "select * from jobPost"
    result = db.execute(temp_query)
    body=result.fetchall()[0][1]

    return render_template('job_post.html', post_id=post_id, result=result, body=body)

if __name__ == '__main__':
    app.run(debug=True)
