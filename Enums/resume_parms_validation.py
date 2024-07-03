from enum import Enum

class Relocation(Enum):
    LIVING_OR_RELOCATION = "living_or_relocation"
    LIVING = "living"
    LIVING_BUT_RELOCATION = "living_but_relocation"
    RELOCATION = "relocation"

class Sex(Enum):
    MALE = "male"
    FEMALE = "female"
    UNKNOWN = "unknown"

class JobSearchStatus(Enum):
    UNKNOWN = "unknown"
    NOT_LOOKING_FOR_JOB = "not_looking_for_job"
    LOOKING_FOR_OFFERS = "looking_for_offers"
    ACTIVE_SEARCH = "active_search"
    HAS_JOB_OFFER = "has_job_offer"
    ACCEPTED_JOB_OFFER = "accepted_job_offer"

class Education(Enum):
    HIGHER = "higher"
    NOT_REQUIRED_OR_NOT_SPECIFIED = "not_required_or_not_specified"
    SPECIAL_SECONDARY = "special_secondary"
    UNFINISHED_HIGHER = "unfinished_higher"
    SECONDARY = "secondary"
    BACHELOR = "bachelor"
    MASTER = "master"
    CANDIDATE = "candidate"
    DOCTOR = "doctor"

class Employment(Enum):
    VOLUNTEER = "volunteer"
    PROBATION = "probation"
    PROJECT = "project"
    PART = "part"
    FULL = "full"

class Experience(Enum):
    NONE = "None"
    BETWEEN1AND3 = "between1And3"
    NO_EXPERIENCE = "noExperience"
    BETWEEN3AND6 = "between3And6"
    MORE_THAN6 = "moreThan6"

class Schedule(Enum):
    FULL_DAY = "fullDay"
    SHIFT = "shift"
    FLY_IN_FLY_OUT = "flyInFlyOut"
    REMOTE = "remote"
    FLEXIBLE = "flexible"
