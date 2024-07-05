from enum import Enum

class Vacancy_Education(Enum):
    NONE = "Пропустить"
    HIGHER = "higher"
    NOT_REQUIRED_OR_NOT_SPECIFIED = "not_required_or_not_specified"
    SPECIAL_SECONDARY = "special_secondary"

class Vacancy_PartTime(Enum):
    NONE = "Пропустить"
    EMPLOYMENT_PART = "employment_part"
    FROM_FOUR_TO_SIX_HOURS_IN_A_DAY = "from_four_to_six_hours_in_a_day"
    START_AFTER_SIXTEEN = "start_after_sixteen"
    EMPLOYMENT_PROJECT = "employment_project"
    ONLY_SATURDAY_AND_SUNDAY = "only_saturday_and_sunday"

class Vacancy_Experience(Enum):
    NONE = "Пропустить"
    BETWEEN1AND3 = "between1And3"
    NO_EXPERIENCE = "noExperience"
    BETWEEN3AND6 = "between3And6"
    MORE_THAN6 = "moreThan6"

class Vacancy_Schedule(Enum):
    NONE = "Пропустить"
    FULL_DAY = "fullDay"
    SHIFT = "shift"
    FLY_IN_FLY_OUT = "flyInFlyOut"
    REMOTE = "remote"
    FLEXIBLE = "flexible"
