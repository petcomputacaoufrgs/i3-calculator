from bs4 import BeautifulSoup

if __name__ == '__main__':
    html = open("Aluno - Histórico do Curso.html")
    soup = BeautifulSoup(html, 'html.parser')

    table = soup.find("table", class_="modelo1")
    result = table.findAll('td')

    table_of_grades = []
    absolute_grades = [0, 0, 0, 0, 0]
    grades_dictionary = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'FF': 4}
    for r in range(0, len(result), 9):
        semester = result[r].string.strip()
        grade = result[r + 2].string.strip()

        if grade != '-':
            absolute_grades[grades_dictionary.get(grade)] += 1
            if len(table_of_grades) > 0:
                encontrado = False
                for i in range(len(table_of_grades)):
                    if semester in table_of_grades[i]:
                        encontrado = True
                        table_of_grades[i][1][grades_dictionary.get(grade)] += 1

                if not encontrado:
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
            else:
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

    for semester in table_of_grades:
        I3 = (10 * semester[1][0] + 8 * semester[1][1] + 6 * semester[1][2]) / sum(semester[1])
        semester.append(I3)

    I3 = (10 * absolute_grades[0] + 8 * absolute_grades[1] + 6 * absolute_grades[2]) / sum(absolute_grades)

    print(table_of_grades)
    print(I3)