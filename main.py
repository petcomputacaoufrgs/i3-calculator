from bs4 import BeautifulSoup
import os

MEETING_MESSAGE = '\033[1;30;46m Bem-vinde a calculadora de I3 \033[m'
CONCLUSION_MESSAGE = '\033[1;30;46m Obrigada por usar o programa! \033[m'


def has_extension(raw_file_name: str) -> bool:
    """ Check if the file name given has an extension
    :param raw_file_name: file's name
    :return: boolean indicating if the file has the extension or not
    """
    if len(raw_file_name.split(".")) == 1:
        return False
    return True


def add_extension(raw_file_name: str, file_extension: str) -> str:
    """ Give the file extension to the file
    :param raw_file_name: file's name
    :param file_extension: extension of the file
    :return: file with the '.csv' extension
    """
    return raw_file_name + file_extension


def get_valid_file_name(message: str, extension: str, need_to_exist=True) -> str:
    """ Get a valid file name (file name that exists in the computer)
    :param need_to_exist: boolean indicating if the files must exist or can be created
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


def continue_process(question: str, default=None) -> bool:
    """ Verify if the process should continue or not based on the user's choice
    :param question: string with the question made
    :param default: default option if no input is given ('y' or 'n') (forces user to enter a valid input if empty)
    :return: return a boolean indicating if the process continues or not
    """
    prompt = question
    if default != None:
        if default == 'y': prompt += ' (Y/n): '
        else: prompt += ' (y/N): '
    else: prompt += ' (y/n): '

    answer = input(prompt).lower()

    if len(answer) == 0 and default != None:
        if default == 'y':
            return True
        else:
            return False

    while answer != 'y' and answer != 'n':
        answer = input('Escolha inválida. Por favor, tente novamente (y/n): ').lower()

    if answer == 'y':
        return True
    else:
        return False


def get_grades(info_table) -> (list[list[list[int]]], list[int]):
    """ Get student grades based on the table with all information
    :param info_table: html table with all data of the classes
    :return: a list with all grades per semester and a list with all grades
    """
    table_of_grades = []
    absolute_grades = [0, 0, 0, 0, 0]
    grades_dictionary = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'FF': 4}

    for r in range(0, len(info_table), 11):
        semester = info_table[r].string.strip()
        grade = info_table[r + 5].string.strip()

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


def calculate_i3(absolute_grades: list) -> float:
    """ Calculate the I3 based on the formula
    I3 = [10 * A_grades + 8 * B_grades + 6 * C_grades]/ total_grades
    Total_grades count A, B, C, D and FF grades
    :param absolute_grades: list with all grades count
    :return: I3 value
    """
    return (10 * absolute_grades[0] + 8 * absolute_grades[1] + 6 * absolute_grades[2]) / sum(absolute_grades)


def save_student_i3(student_info, destination_file: str):
    """ Save the I3 obtained in the file given
    :param student_info: instance of Student with the necessary information
    :param destination_file: file where the data will be stored
    :return: void
    """
    file = open(destination_file, "a")
    file.write(f'Candidato: {student_info.name}, I3: {student_info.I3}\n')
    for semester in student_info.grades_per_semester:
        file.write(f'I3 {semester[0]}: {semester[2]}\n')
    # file.write('\n')
    file.close()


class Student:
    def __init__(self, file_name):
        html = open(file_name)
        soup = BeautifulSoup(html, 'html.parser')

        self.name = soup.find("div", class_="nomePessoa").string.strip()
        print(self.name)
        info_table = soup.find("table", class_="modelo1").findAll('td')
        html.close()

        table_of_grades, absolute_grades = get_grades(info_table)

        self.grades_per_semester = table_of_grades

        for semester in table_of_grades:
            i3 = calculate_i3(semester[1])
            semester.append(i3)

        self.I3 = calculate_i3(absolute_grades)


if __name__ == '__main__':
    print(MEETING_MESSAGE)
    over = False
    info_file = get_valid_file_name(
        'Insira o nome do arquivo .html do histórico do curso do aluno (com ou sem extensão): ', '.html')
    student = Student(info_file)

    save_file = get_valid_file_name(
        'Insira o nome do arquivo .txt onde os dados obtidos serão salvos (com ou sem extensão): ', '.txt', False)

    while not over:
        save_student_i3(student, save_file)

        if not continue_process('Deseja continuar lendo arquivos?', 'y'):
            over = True
            continue

        info_file = get_valid_file_name('Insira o novo arquivo .html a ser lido (com ou sem extensão): ', '.html')

        if continue_process('Deseja salvar os dados no mesmo arquivo .txt de antes?', 'y'):
            continue

        save_file = get_valid_file_name('Insira o nome do novo arquivo .txt (com ou sem extensão): ', '.txt', False)
    print(CONCLUSION_MESSAGE)
