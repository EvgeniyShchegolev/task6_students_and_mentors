from functools import reduce


class Person:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.grades = {}

    def _total_grade(self):
        result, n_grades = 0, 0
        for grade in self.grades.values():
            result += sum(grade)
            n_grades += len(grade)
        if not n_grades:
            print('Нет оценок по курсам, невозможно вычислить среднюю оценку')
            return
        return round(result / n_grades, 1)


class Student(Person):
    def __init__(self, name, surname, gender):
        super().__init__(name, surname)
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []

    def rate_lect(self, lect, course, grade):
        if isinstance(lect, Lecturer) and course in lect.courses_attached and course in self.courses_in_progress:
            if course in lect.grades:
                lect.grades[course] += [grade]
            else:
                lect.grades[course] = [grade]
        else:
            return 'Ошибка ввода данных'

    def __str__(self):
        res = f'Имя: {self.name}\n' \
              f'Фамилия: {self.surname}\n' \
              f'Средняя оценка за домашние задания: {self._total_grade()}\n' \
              f'Курсы в процессе изучения: {", ".join(self.courses_in_progress)}\n' \
              f'Завершённые курсы: {", ".join(self.finished_courses)}'
        return res

    def __lt__(self, other):
        if not isinstance(other, Student):
            return 'Ошибка ввода данных!'
        return (self._total_grade()) < (other._total_grade())


class Mentor(Person):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.courses_attached = []


class Lecturer(Mentor):
    def __str__(self):
        res = f'Имя: {self.name}\n' \
              f'Фамилия: {self.surname}\n' \
              f'Средняя оценка за лекции: {self._total_grade()}'
        return res

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            return 'Ошибка ввода данных!'
        return (self._total_grade()) < (other._total_grade())


class Reviewer(Mentor):
    def rate_hw(self, stud, course, grade):
        if isinstance(stud, Student) and course in self.courses_attached and course in stud.courses_in_progress:
            if course in stud.grades:
                stud.grades[course] += [grade]
            else:
                stud.grades[course] = [grade]
        else:
            return 'Ошибка ввода данных'

    def __str__(self):
        res = f'Имя: {self.name}\n' \
              f'Фамилия: {self.surname}'
        return res


def total_grade(course, *stud_or_lect):
    """
    Функция позволяющая подсчитать среднюю оценку за курс либо студентов, либо лекторов.
    Принимает в качестве аргументов название курса и неограниченное количество экземпляров либо только студентов
    либо только лекторов, в ином случае выдаёт ошибку.
    В зависимости от этого выводит разное сообщение с оценкой и для студентов, и для лекторов.
    """
    is_students = reduce(lambda x, y: x and y, list(isinstance(student, Student) for student in stud_or_lect))
    is_lecturers = reduce(lambda x, y: x and y, list(isinstance(lecturer, Lecturer) for lecturer in stud_or_lect))
    if is_students or is_lecturers:
        result, n_grades = 0, 0
        for person in stud_or_lect:
            if course in person.grades.keys():
                result += sum(person.grades[course])
                n_grades += len(person.grades[course])
        if not n_grades:
            print('Нет оценок по курсу, невозможно вычислить среднюю оценку')
            return
        if is_students:
            text = f'Средняя оценка всех студентов за домашние задания по курсу {course}: '
        else:
            text = f'Средняя оценка всех лекторов за лекции по курсу {course}: '
        print(text + str(round(result / n_grades, 1)))
        return
    print('Ошибка ввода данных!')
    return


student1 = Student('Tim', 'Stone', 'male')
student1.courses_in_progress += ['Python', 'JavaScript']
student1.finished_courses += ['Основы основ', 'Git']
student2 = Student('Eva', 'Kernel', 'female')
student2.courses_in_progress += ['JavaScript', 'CSS', 'HTML']
student3 = Student('Anna', 'Ivanova', 'female')
student3.courses_in_progress += ['Python', 'HTML']

lecturer1 = Lecturer('Alex', 'Oldman')
lecturer1.courses_attached += ['Python', 'JavaScript']
lecturer2 = Lecturer('Jane', 'Ivanova')
lecturer2.courses_attached += ['JavaScript', 'CSS', 'HTML']

reviewer1 = Reviewer('Tom', 'Begins')
reviewer1.courses_attached += ['Python']
reviewer2 = Reviewer('Elena', 'Milkova')
reviewer2.courses_attached += ['JavaScript']
reviewer3 = Reviewer('James', 'Kuler')
reviewer3.courses_attached += ['CSS', 'HTML']

reviewer1.rate_hw(student1, 'Python', 9)
reviewer1.rate_hw(student1, 'Python', 6)
reviewer2.rate_hw(student1, 'JavaScript', 8)
reviewer3.rate_hw(student3, 'HTML', 6)

student1.rate_lect(lecturer1, 'Python', 8)
student2.rate_lect(lecturer1, 'Python', 8)
student3.rate_lect(lecturer1, 'JavaScript', 9)
student3.rate_lect(lecturer2, 'HTML', 7)

print(reviewer3)
print(lecturer2)
print(student1)
print(lecturer1 < lecturer2)
print(student1 < student3)

total_grade('Python', student1, student2, student3)
total_grade('Python', lecturer1, lecturer2)
