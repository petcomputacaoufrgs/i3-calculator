from bs4 import BeautifulSoup
import os


def has_extension(raw_file_name: str) -> bool:
    """Check if the file name given has an extension
    :param raw_file_name: file's name
    :return: boolean indicating if the file has the extension or not
    """
    if len(raw_file_name.split(".")) == 1:
        return False
    return True


def add_extension(raw_file_name: str, file_extension: str) -> str:
    """Give the file extension to the file
    :param raw_file_name: file's name
    :param file_extension: extension of the file
    :return: file with the '.csv' extension
    """
    return raw_file_name + file_extension


def get_valid_file_name(message, extension, need_to_exist=True) -> str:
    """ Get a valid file name (file name that exists in the computer)
    :param message: question soliciting the specific file needed
    :param extension: extension of the file
    :return: valid file name
    """
    found = False
    input_file = input(message)

    while not found:
        if not has_extension(input_file):
            input_file = add_extension(input_file, extension)
        if not need_to_exist or os.path.exists(input_file):
            found = True
        else:
            input_file = input('Arquivo não encontrado. \nPor favor, tente novamente: ')
    return input_file


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
    file.write(f"""Candidato: {student_info.name}
I3: {student_info.I3}
I3 por semestre: 
{student_info.grades_per_semester}

""")
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
    # Tem que ser o histórico do curso
    over = False
    input_file = get_valid_file_name(
        'Insira o nome do arquivo .html do histórico do curso do aluno (com ou sem extensão): ', '.html')
    student = Student(input_file)

    save_file = get_valid_file_name(
        'Insira o nome do arquivo .txt onde os dados obtidos serão salvos (com ou sem extensão): ', '.txt', False)

    while not over:
        save_info(student, save_file)
        continue_process = input('Deseja continuar lendo arquivos? (y/n): ')
        if continue_process == 'n':
            over = True
            continue
        input_file = get_valid_file_name('Insira o novo arquivo .html a ser lido (com ou sem extensão): ', '.html')
        use_same_file = input('Deseja salvar os dados no mesmo arquivo .txt de antes? (y/n): ')
        if use_same_file == 'y':
            continue
        save_file = get_valid_file_name('Insira o nome do novo arquivo .txt (com ou sem extensão): ', '.txt', False)
