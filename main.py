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


def calculate_i3(grade_table) -> float:
    """ Calculate the overall I3 based on the formula
    I3 = [10 * A_grades + 8 * B_grades + 6 * C_grades] / total_grades
    Total_grades count A, B, C, D and FF grades
    :param grade_table: table of all grades by semester
    :return: I3 value
    """
    numerator = 0
    denominator = 0

    for semester in grade_table:
        for grade in grade_table[semester]:
            if grade == 'A': numerator += 10
            elif grade == 'B': numerator += 8
            elif grade == 'C': numerator += 6

            if grade != '-': denominator += 1

    if denominator != 0: return numerator/denominator
    else: return 0


def calculate_semester_i3(grade_list) -> float:
    """ Calculate a semester's I3 based on the formula
    I3 = [10 * A_grades + 8 * B_grades + 6 * C_grades] / total_grades
    Total_grades count A, B, C, D and FF grades
    :param grade_table: list of grades for a specific semester
    :return: I3 value
    """
    numerator = 0
    denominator = 0

    for grade in grade_list:
        if grade == 'A': numerator += 10
        elif grade == 'B': numerator += 8
        elif grade == 'C': numerator += 6

        if grade != '-': denominator += 1

    if denominator != 0: return numerator/denominator
    else: return 0


def save_student_i3(student_info, destination_file: str):
    """ Save the I3 obtained in the file given
    :param student_info: instance of Student with the necessary information
    :param destination_file: file where the data will be stored
    :return: void
    """
    file = open(destination_file, "a")
    file.write(f'Candidato: {student_info.name}, I3: {student_info.I3}\n')
    for semester in student_info.I3_by_semester:
        file.write(f'I3 {semester}: {student_info.I3_by_semester[semester]}\n')
    file.close()


def get_grades_from_html_table(table):
    cols = len(table.find_all('th'))
    rows = len(table.find_all('tr'))
    col_semester = len(table.find(string="Per�odo Letivo").find_all_previous('th')) - 1
    col_grade = len(table.find(string="Conceito").find_all_previous('th')) - 1
    grades = {}

    all_rows = table.find('tr').find_next_siblings('tr')

    new_semester = ""
    for row in all_rows:
        cells = row.find_all('td')
        semester = cells[col_semester].string.strip()
        grade = cells[col_grade].string.strip()

        if new_semester != semester:
            grades[semester] = [grade]
            new_semester = semester
        else:
            grades[semester].append(grade)

    return grades


class Student:
    def __init__(self, file_name):
        html = open(file_name)
        soup = BeautifulSoup(html, 'html.parser')

        self.name = soup.find("div", class_="nomePessoa").string.strip()
        print(self.name)
        grade_table = get_grades_from_html_table(soup.find("table", class_="modelo1"))
        html.close()

        self.I3 = calculate_i3(grade_table)
        self.I3_by_semester = {}

        for semester in grade_table:
            i3 = calculate_semester_i3(grade_table[semester])
            if i3 != 0:
                self.I3_by_semester[semester] = calculate_semester_i3(grade_table[semester])


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
