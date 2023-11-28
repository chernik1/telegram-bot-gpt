import re
from config import Lesson
from dataclasses import dataclass
import dataclasses


@dataclasses.dataclass
class Math(Lesson):
    name = 'Math'
    short_name = 'm'
    directory = 'math'
    regex_dict = {
        'regex': r'\d{1,2}\..+?(?=\n|$)',
    }

@dataclasses.dataclass
class Programming(Lesson):
    name = 'Programming'
    short_name = 'p'
    directory = 'programming'
    regex_dict = {
        'regex': r'\d{1,2}\..+?(?=\n|$)',
    }

@dataclasses.dataclass
class Economics(Lesson):
    name = 'Economics'
    short_name = 'e'
    directory = 'economics'
    regex_dict = {
        'regex': r'\d{1,2}\..+?(?=\n|$)',
    }

@dataclasses.dataclass
class History(Lesson):
    name = 'History'
    short_name = 'h'
    directory = 'history'
    regex_dict = {
        'regex': r'\d{1,2}\..+?(?=\n|$)',
    }

@dataclasses.dataclass
class English(Lesson):
    name = 'English'
    short_name = 'en'
    directory = 'english'
    regex_dict = {
        'regex': r'\d{1,2}\..+?(?=\n|$)',
    }

@dataclasses.dataclass
class Biology(Lesson):
    name = 'Biology'
    short_name = 'b'
    directory = 'biology'
    regex_dict = {
        'regex': r'\d{1,2}\..+?(?=\n|$)',
    }

@dataclasses.dataclass
class Chemistry(Lesson):
    name = 'Chemistry'
    short_name = 'c'
    directory = 'chemistry'
    regex_dict = {
        'regex': r'\d{1,2}\..+?(?=\n|$)',
    }

@dataclasses.dataclass
class Physics(Lesson):
    name = 'Physics'
    short_name = 'ph'
    directory = 'physics'
    regex_dict = {
        'regex': r'\d{1,2}\..+?(?=\n|$)',
    }

@dataclasses.dataclass
class Belorussian(Lesson):
    name = 'Belorussian'
    short_name = 'b'
    directory = 'belorussian'
    regex_dict = {
        'regex': r'\d{1,2}\..+?(?=\n|$)',
    }

@dataclasses.dataclass
class MathAnalysis(Math):
    directory = f'{Math.directory}\\math_analysis'

@dataclasses.dataclass
class MathGeometryAndAlgebra(Math):
    directory = f'{Math.directory}\\math_geometry_and_algebra'
