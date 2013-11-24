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

from os import remove
from os.path import dirname, exists, splitext
from shutil import copyfile

def needsReprocessing(auxFilename, auxBackupFilename, logFile):
    if not exists(auxFilename):
        logFile.write("\n.aux file does not exist - signaling reprocessing...")
        return True
    if not exists(auxBackupFilename):
        logFile.write("\n.aux.bk backup file does not exist - signaling reprocessing...")
        return True
    if open(auxFilename).read() != open(auxBackupFilename).read():
        logFile.write("\n.aux file and .aux.bk backup files differ - signaling reprocessing...")
        return True
    logFile.write("\n.aux and .aux.bk files are the same - signaling success...")
    return False

def generatePdf(texFilename, system, glossary=False):
    errors = []
    warnings = []

    texFilePieces = splitext(texFilename)
    if texFilePieces[1] != ".tex":
        return (["You must specify a LaTeX file ending in .tex"], [])

    logFilename = texFilePieces[0] + '.log'
    logFile = open(logFilename, 'w')

    auxFilename = texFilePieces[0] + '.aux'
    auxBackupFilename = auxFilename + '.bk'

    workingDir = dirname(texFilePieces[0])
    runNumber = 0
    try:
        remove(auxFilename)
        remove(auxBackupFilename)
    except:
        pass

    while needsReprocessing(auxFilename, auxBackupFilename, logFile):
        try:
            copyfile(auxFilename, auxBackupFilename)  # re-run until they are the same
        except:
            pass

        print 'Starting run number %d' % runNumber
        logFile.write('\n===== STARTING RUN NUMBER %d =====' % runNumber)
        try:
            remove(texFilePieces[0] + '.pdf')
        except:
            pass

        if glossary:
            print '- Calling makeglossaries...'
            logFile.write('\n\n===== Making Glossaries (1): makeglossaries %s... =====\n' % texFilePieces[0])
            system.runCommand(['makeglossaries', texFilePieces[0]], out=logFile)

        print '- Generating PDF...'
        logFile.write('\n\n===== Calling XeLaTeX (2): xelatex -synctex=0 -interaction=nonstopmode --src-specials "%s" =====\n' % texFilename)
        logFile.flush()
        system.runCommand(['xelatex',
                           '-synctex=0',
                           '-interaction=nonstopmode',
                           '--src-specials',
                           texFilename],
                          out=logFile,
                          workingDir=workingDir)

        # no .aux file means something went wrong
        if not exists(auxFilename):
            return (['Something went wrong - no .aux file was generated!'], [])

        logFile.write('\n===== Done with run number %d =====\n\n' % runNumber)
        runNumber += 1

    print 'Removing *.aux files...'
    remove(auxFilename)
    remove(auxBackupFilename)

    print 'Done.'

    return (errors, warnings)
