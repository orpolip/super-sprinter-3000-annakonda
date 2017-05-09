# All the neccessary imports:

from flask import *
import csv

# Functions what the program needs to handle .csv operations


def read_from_csv(file_name):
    """This function generates the table, returns with the lists of the rows in the text"""
    table = []
    with open(file_name, "r") as text:
        for row in text:
            row_unformatted = row.replace("\n", "")
            words = row_unformatted.split(',')
            table.append(words)
    return table


def write_to_csv(file_name, table):
    """With this function we can write into th csv file"""
    with open(file_name, "w") as f:
        for item in table:
            story = ','.join(item)
            f.write(story + "\n")


def generate_id(table):
    """A small function what give us(returns) a new ID when we add a new story"""
    new_id = [0]
    for row in table:
        new_id.append(int(row[0]))
    new_id = max(new_id) + 1

    return str(new_id)

# My CODE:


app = Flask(__name__)


@app.route('/')
def root():
    table = read_from_csv("stories.csv")
    return render_template('list.html', table=table)


@app.route("/story", methods=['GET', 'POST'])
def new_user_story():
    if request.method == 'POST':
        table = read_from_csv("stories.csv")
        new_story = []
        new_story.append(generate_id(table))
        new_story.append(request.form['title'])
        new_story.append(request.form['comments_story'])
        new_story.append(request.form['comments_acc'])
        new_story.append(request.form['Business_value'])
        new_story.append(request.form['estimation'])
        new_story.append(request.form['status'])
        table.append(new_story)
        write_to_csv("stories.csv", table)

        return render_template("list.html", table=table)
    else:
        return render_template("form.html")


@app.route('/story/<story_id>', methods=['GET', 'POST'])
def update_user_story(story_id):
    if request.method == 'POST':
        table = read_from_csv("stories.csv")
        for row in table:
            if row[0] == story_id:
                row[1] = request.form['title']
                row[2] = request.form['comments_story']
                row[3] = request.form['comments_acc']
                row[4] = request.form['Business_value']
                row[5] = request.form['estimation']
                row[6] = request.form['status']
        write_to_csv("stories.csv", table)
        return render_template("list.html", table=table)
    else:
        return render_template("form2.html")


@app.route('/story/<story_id>/delete', methods=["POST"])
def delete_user_story(story_id):
    table = read_from_csv("stories.csv")
    with open('stories.csv', 'w') as f:
        for row in table:
            if row[0] == story_id:
                del row
            else:
                writer = csv.writer(f)
                writer.writerow(row)
        return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
