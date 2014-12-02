# /usr/bin/env python

# Copyright 2012, 2013 J. Luke Scott
# This file is part of latex-contracts.

# latex-contracts is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# latex-contracts is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with latex-contracts.  If not, see <http://www.gnu.org/licenses/>.

import codecs
import datetime
import locale
import re

# everything should be utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from jinja2 import Environment, FileSystemLoader
from json import dumps
from os.path import dirname, realpath
from latex_python.XetexWrapper import generatePdf

locale.setlocale(locale.LC_ALL, '')

DEFAULT_ENVIRONMENT_PARAMETERS = {'block_start_string': '[[[',  # the only lower-case brackets
                                  'block_end_string': ']]]',
                                  'variable_start_string': '(((',  # most intuitive for variable enclosing
                                  'variable_end_string': ')))',
                                  'comment_start_string':'/*',
                                  'comment_end_string':'*/',
                                  }

LATEX_SUBS = (
    (re.compile(r'\\'), r'\\textbackslash'),
    (re.compile(r'([{}_#%&$])'), r'\\\1'),
    (re.compile(r'~'), r'\~{}'),
    (re.compile(r'\^'), r'\^{}'),
    (re.compile(r'\.\.\.+'), r'\\ldots'),
)

# normally you'd use this in conjunction with escapeTex(): bold(escapeTex(stringValue))
def bold(value):
    newval = value.__str__()  # in case we get a Person, Property, etc.
    return '\\textbf{%s}' % newval
    
def escapeTex(value):
    newval = value.__str__()  # in case we get a Person, Property, etc.
    for pattern, replacement in LATEX_SUBS:
        newval = pattern.sub(replacement, newval)
    return newval


def inflate(value, objectTypes):
    'inflate an object from a dict that describes it. The value migt be a primitive or a JsonSerializable object.'
    if isinstance(value, dict) and '_type' in value.keys():
        # it's a JsonSerializable object. inflate it recursively.
        kwargs = {}
        for key in value.keys():
            if key == '_type':
                continue
            kwargs[key] = inflate(value[key], objectTypes)
        try:
            result = eval(value['_type'])(**kwargs)
        except:
            # module not loaded - try loading it dynamically from possibleSubclasses
            result = objectTypes[value['_type']](**kwargs)
        return result
    elif isinstance(value, dict):
        # it's a regular dict. Cycle through the keys and inflate them all into objects as necessary
        return {k: inflate(v, objectTypes) for k, v in value.items()}
    elif isinstance(value, list):
        return [inflate(v, objectTypes) for v in value]
    else:
        return value


class JsonSerializable(object):
    '''
    a base class for objects which can be serialized using object.__json__().
    (currently, it's just getJsonValue())

    Any field starting with an underscore (_) is considered a 'meta' field,
    and will not be serialized. This allows Python objects to maintain state
    for their operation which is not relevant to their serialized/persisted state.
    '''

    def __init__(self, **kwargs):
        self._required = []
        # set fields by dict constructor
        for arg in kwargs:
            self.__dict__[arg] = kwargs[arg]

    def getJsonString(self):
        result = dumps(self.getJsonCompatibleDict(), indent=4)
        return result

    def getJsonCompatibleDict(self):
        result = {'_type': self.__class__.__name__}
        for field in self.__dict__.keys():
            if field[:1] == '_':
                # skip meta-fields (begins with _)
                continue
            value = getattr(self, field, None)
            if value == None:
                continue
            result[field] = self.getJsonValue(value)
        # SPECIAL CASE: add the MongoDB ID if it exists.
        # other ways of handling this would have been more hacky.
        if '_id' in self.__dict__:
            result['_id'] = self._id
        return result

    def getJsonValue(self, value):
        if isinstance(value, list):
            return [self.getJsonValue(item) for item in value]
        elif isinstance(value, dict):
            return {k: self.getJsonValue(v) for k, v in value.items()}
        elif isinstance(value, JsonSerializable):
            # not a json-ic primitive. Must be converted using recursive call.
            return value.getJsonCompatibleDict()
        else:
            return value

    def equals(self, other):
        # get Python dict representation
        myJson = self.getJsonCompatibleDict()
        otherJson = other.getJsonCompatibleDict()
        # compare naturally
        return myJson == otherJson

    def validate(self, obj=None, prefix=''):
        if obj == None:
            # start recursion at self
            obj = self
        errors = []
        requiredFields = getattr(obj, '_required', [])
        for requiredField in requiredFields:
            if not requiredField in obj.__dict__:
                errors.append('%s.%s' % (prefix, requiredField))
        # recurse
        try:
            for field in sorted(obj.__dict__):
                child = obj.__dict__[field]
                if field[:1] != '_' and child != None and (isinstance(child, object) or type(child) == dict):
                    # this object member is either a meta (_) field or is not an object or dict,
                    # and so is not able to have 'required fields'
                    errors += self.validate(child, '%s.%s' % (prefix, field))
        except:
            # probably a list
            pass

        return errors

class JinjaTexDocument(JsonSerializable):
    def __init__(self, templateModule=None, searchPath=None, **kwargs):
        super(JinjaTexDocument, self).__init__(**kwargs)

        environmentParameters = {}
        environmentParameters.update(DEFAULT_ENVIRONMENT_PARAMETERS)
        environmentParameters['loader'] = FileSystemLoader(searchPath or realpath(dirname(__file__)))
        self.environment = Environment(**environmentParameters)
        self.environment.filters['escapeTex'] = escapeTex

        templateBaseName = self.__class__.__name__
        self.classTemplate = self.environment.get_template(templateBaseName + '.cls')
        self.texTemplate = self.environment.get_template(templateBaseName + '.tex')
        self.templateModule = templateModule

    def applyTemplateContentIfNecessary(self):
        if self.templateModule is not None:
            templateModule = self.templateModule
            self.templateModule = None  # to avoid recursion
            templateModule.addContent(self)

    def set(self, **kwargs):
        self.__dict__.update(kwargs)

    def generate(self, outputFilenameBase, system, variables={}):
        # apply the template if it hasn't been applied already
        # (this will be the case if no custom clauses have been added)
        self.applyTemplateContentIfNecessary()

        errors = self.validate()
        if errors:
            return (errors, [], None)  # errors, warnings, filename

        extension = outputFilenameBase[-4:].lower()
        if extension == '.tex' or extension == '.pdf':
            outputFilenameBase = outputFilenameBase[0:-4]

        classFilename = outputFilenameBase + '.cls'
        classFile = codecs.open(classFilename, 'w', 'utf-8')
        today = datetime.date.today()
        classFile.write('''
            \\NeedsTeXFormat{LaTeX2e}[1999/09/01]
            \\ProvidesClass{%s}[%4d/%2d/%2d J Luke Scott, Copyright (C) %4d]
        ''' % (outputFilenameBase, today.year, today.month, today.day, today.year))
        output = self.classTemplate.render(variables)
        classFile.write(output)
        classFile.close()

        texFilename = outputFilenameBase + '.tex'
        texFile = codecs.open(texFilename, 'w', 'utf-8')
        texFile.write('''
            \\documentclass{%s}
        ''' % (outputFilenameBase))
        output = self.texTemplate.render(variables)
        texFile.write(output)
        texFile.close()

        return generatePdf(texFilename=texFilename, system=system)

class Date(JsonSerializable):
    # NOTE: true/false not actually measured because __init__ is overridden
    def __init__(self, year=None, month=None, day=None):
        self._required = ['year', 'month', 'day']
        today = datetime.date.today()
        self.year = year or today.year
        self.month = month or today.month
        self.day = day or today.day

    # replaces \dateYMD{y}{m}{d}
    def __str__(self, *args, **kwargs):
        return "\\formatdate{%d}{%d}{%d}" % (self.day, self.month, self.year)


class Money(JsonSerializable):
    def __init__(self, amount):
        self._required = ['amount']
        self.amount = amount

    def __str__(self, *args, **kwargs):
        # we need to insert our own $ so that it's not confused
        result = locale.currency(self.amount, symbol=True, grouping=True)
        return result

class Percent(JsonSerializable):
    def __init__(self, amount):
        self._required = ['amount']
        self.amount = amount

    def __str__(self, *args, **kwargs):
        return "%d%%" % self.amount
