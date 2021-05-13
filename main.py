from bs4 import BeautifulSoup


def calculate_grades(info_table):
    table_of_grades = []
    absolute_grades = [0, 0, 0, 0, 0]
    grades_dictionary = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'FF': 4}

    for r in range(0, len(info_table), 9):
        semester = info_table[r].string.strip()
        grade = info_table[r + 2].string.strip()

        if grade != '-':
            absolute_grades[grades_dictionary.get(grade)] += 1
            found = False
            if len(table_of_grades) > 0:
                for i in range(len(table_of_grades)):
                    if semester in table_of_grades[i]:
                        found = True
                        table_of_grades[i][1][grades_dictionary.get(grade)] += 1

            if not found or len(table_of_grades) < 1:
                if grade == 'A':
                    table_of_grades.append([semester, [1, 0, 0, 0, 0]])
                elif grade == 'B':
                    table_of_grades.append([semester, [0, 1, 0, 0, 0]])
                elif grade == 'C':
                    table_of_grades.append([semester, [0, 0, 1, 0, 0]])
                elif grade == 'D':
                    table_of_grades.append([semester, [0, 0, 0, 1, 0]])
                elif grade == 'FF':
                    table_of_grades.append([semester, [0, 0, 0, 0, 1]])
    return table_of_grades, absolute_grades


def calculate_i3(absolute_grades):
    return (10 * absolute_grades[0] + 8 * absolute_grades[1] + 6 * absolute_grades[2]) / sum(absolute_grades)


def save_info(student_info, destination_file):
    file = open(destination_file, "a")
    file.write(f"""
Candidato: {student_info.name}
I3: {student_info.I3}
I3 por semestre: 
{student_info.grades_per_semester}""")
    file.close()


class Student:
    def __init__(self, file_name):
        html = open(file_name)
        soup = BeautifulSoup(html, 'html.parser')

        self.name = soup.find("div", class_="nomePessoa").string.strip()
        info_table = soup.find("table", class_="modelo1").findAll('td')

        table_of_grades, absolute_grades = calculate_grades(info_table)

        self.grades_per_semester = table_of_grades

        for semester in table_of_grades:
            i3 = calculate_i3(semester[1])
            semester.append(i3)

        self.I3 = calculate_i3(absolute_grades)


if __name__ == '__main__':
    student = Student("historico.html")
    save_info(student, 'information.txt')
