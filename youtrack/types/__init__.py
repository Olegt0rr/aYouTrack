from .base import *
from .connection import *
from .issue import *

types = {
    'base': YouTrackObject,
    'issue': Issue,
    'issues': IssueList,
}