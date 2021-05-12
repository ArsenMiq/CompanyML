from __future__ import print_function
from PreparingData import trainingData, testingData, getHeaderList

training_data = trainingData("data.csv", 125, 146)

header = getHeaderList("data.csv")


def unique_vals(rows, col):
    return set([row[col] for row in rows])


def class_counts(rows, index):
    counts = {}
    for row in rows:
        label = row[index]
        if label not in counts:
            counts[label] = 0
        counts[label] += 1
    return counts


print(class_counts(training_data, 2))


def is_numeric(value):
    return isinstance(value, int) or isinstance(value, float)


class Question:

    def __init__(self, column, value):
        self.column = column
        self.value = value

    def match(self, example):
        val = example[self.column]
        if is_numeric(val):
            return val >= self.value
        else:
            return val == self.value

    def __repr__(self):
        condition = "=="
        if is_numeric(self.value):
            condition = ">="
        return "Is %s %s %s?" % (
            header[self.column], condition, str(self.value))


def partition(rows, question):
    true_rows, false_rows = [], []
    for row in rows:
        if question.match(row):
            true_rows.append(row)
        else:
            false_rows.append(row)
    return true_rows, false_rows


def gini(rows):
    counts = class_counts(rows, 1)
    impurity = 1
    for lbl in counts:
        prob_of_lbl = counts[lbl] / float(len(rows))
        impurity -= prob_of_lbl ** 2
    return impurity


def info_gain(left, right, current_uncertainty):
    p = float(len(left)) / (len(left) + len(right))
    return current_uncertainty - p * gini(left) - (1 - p) * gini(right)


def find_best_split(rows):
    best_gain = 0
    best_question = None
    current_uncertainty = gini(rows)
    n_features = len(rows[0]) - 110

    for col in range(n_features):

        values = set([row[col] for row in rows])

        for val in values:

            question = Question(col, val)
            print(question)

            true_rows, false_rows = partition(rows, question)

            if len(true_rows) == 0 or len(false_rows) == 0:
                continue

            gain = info_gain(true_rows, false_rows, current_uncertainty)

            if gain >= best_gain:
                best_gain, best_question = gain, question

    return best_gain, best_question


class Leaf:

    def __init__(self, rows):
        self.predictions = class_counts(rows, 1)


class Decision_Node:
    def __init__(self,
                 question,
                 true_branch,
                 false_branch):
        self.question = question
        self.true_branch = true_branch
        self.false_branch = false_branch


def build_tree(rows):
    gain, question = find_best_split(rows)

    if gain == 0:
        return Leaf(rows)

    true_rows, false_rows = partition(rows, question)

    true_branch = build_tree(true_rows)

    false_branch = build_tree(false_rows)

    return Decision_Node(question, true_branch, false_branch)


def print_tree(node, spacing=""):
    if isinstance(node, Leaf):
        print(spacing + "Predict", node.predictions)
        return

    print(spacing + str(node.question))

    print(spacing + '--> True:')
    print_tree(node.true_branch, spacing + "  ")

    print(spacing + '--> False:')
    print_tree(node.false_branch, spacing + "  ")


def classify(row, node):
    if isinstance(node, Leaf):
        return node.predictions

    if node.question.match(row):
        return classify(row, node.true_branch)
    else:
        return classify(row, node.false_branch)


def print_leaf(counts):
    total = sum(counts.values()) * 1.0
    probs = {}
    for lbl in counts.keys():
        probs[lbl] = str(int(counts[lbl] / total * 100)) + "%"
    return probs


def findReason(row):
    year = row[3]
    score = row[4]
    employee_count = row[9]
    skill_score = row[73]

    result = ""

    print(Question(3, year))

    if (year != "No Info"):
        if (int(year) < getAverageYears()):
            result = result + "Worked less years, "
        else:
            result = result + "Worked more years, "
    else:
        result = result + "Worked less years, "

    print(Question(3, score))
    print(score)
    if (score != " "):
        if (float(score) < getAverageScore()):
            result = result + "have small score, "
        else:
            result = result + "have big score, "
    else:
        result = result + "have small score, "

    print(Question(3, employee_count))

    if (employee_count != " "):
        if (float(employee_count) < getAverageEmployeeCount()):
            result = result + "the employees are not enough, "
        else:
            result = result + "the employees are enough, "
    else:
        result = result + "the employees are not enough, "

    print(Question(3, skill_score))

    if (skill_score != "No Info"):
        if (float(skill_score) < getAverageSkillScore()):
            result = result + "skill score is less than expected!"
        else:
            result = result + "skill score is very big!"
    else:
        result = result + "skill score is less than expected!"

    return result


def getAverageYears():
    avr = 0
    count = 0
    for row in training_data:
        count += 1
        if (row[3] != "No Info"):
            avr = avr + int(row[3])
    print("The years average is - ", avr / count)
    return avr / count


def getAverageEmployeeCount():
    avr = 0
    count = 0
    for row in training_data:
        count += 1
        if (row[9] != " "):
            avr = avr + float(row[9])
    print("The employees average is - ", avr / count)
    return avr / count


def getAverageScore():
    avr = 0
    count = 0
    for row in training_data:
        count += 1
        if (row[4] != " "):
            avr = avr + float(row[4])
    print("The score average is - ", avr / count)
    return avr / count


def getAverageSkillScore():
    avr = 0
    count = 0
    for row in training_data:
        count += 1
        if (row[73] != "No Info"):
            avr = avr + float(row[73])
    print("The skill average is - ", avr / count)
    return avr / count


if __name__ == '__main__':
    my_tree = build_tree(training_data)

    q = Question(1, 'Success')
    print(q)
    print_tree(my_tree)

    true_rows, false_rows = partition(training_data, Question(1, 'Success'))
    print(true_rows)
    print(false_rows)

    best_gain, best_question = find_best_split(training_data)
    print("\n\nBest question")
    print(best_question)
    print("\n\nBest gain")
    print(best_gain)

    testing_data = testingData("data.csv", 56, 148)

    print("\n\nThe company tree\n")
    print_tree(my_tree)
    print_leaf(classify(training_data[0], my_tree))

    print(class_counts(training_data, 2))

    getAverageYears()

    for row in testing_data:
        print("\n\n")
        print(Question(1, row[1]))
        print("Actual: %s. Predicted: %s. Because: %s" % (row[0], print_leaf(classify(row, my_tree)), findReason(row)))
