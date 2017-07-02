#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import random
import time

DEBUG = False
BIG = False
BIGPOLYNOM = 1000000

# ##############################################################################
# Polynom Generator
# ##############################################################################

def generatePolynom(termRangeFrom=1, termRangeTo=10, numberRange=100):
    """Generate new polynom, default Range from 1 to 10, numberRange = 100"""
    global BIGPOLYNOM
    countOfTerms = random.randrange(termRangeFrom, termRangeTo)
    i = 0
    if termRangeTo >= BIGPOLYNOM:
        print "generating big polynom... " + str(BIGPOLYNOM) + ' terms'
    while i < countOfTerms:
        coefficient = random.randrange(2, numberRange)
        exponent = random.randrange(2, numberRange)
        constant = exponent
        typeOfTerm = random.randrange(0, 3)
        sign = random.choice('-+')
        if typeOfTerm == 0: # 3x^2
            if sign == '-':
                newTerm = Term(-1 * coefficient, exponent)
            else:
                newTerm = Term(coefficient, exponent)
        elif typeOfTerm == 1: # 2x
            if sign == '-':
                newTerm = Term(-1 * constant, 0)
            else:
                newTerm = Term(constant, 0)
        elif typeOfTerm == 2: # x^2
            if sign == '-':
                newTerm = Term(-1 * constant, 1)
            else:
                newTerm = Term(constant, 1)
        i += 1
        if termRangeTo < BIGPOLYNOM:
            print recreateTerm(newTerm.coefficient, newTerm.exponent),
        yield newTerm

def recreateTerm(coefficient, exponent):
    """Recreate one term from coefficient and exponent"""
    if exponent == 0:
        if coefficient > 0:
            return('+ ' + str(coefficient))
        elif coefficient == 0:
            return ''
        else:
            return('- ' + str(coefficient * -1))
    elif exponent == 1:
        if coefficient == 1:
            return('+ x ')
        elif coefficient == -1:
            return('- x ')
        else:
            if coefficient > 0:
                return('+ ' + str(coefficient) + 'x')
            elif coefficient == 0:
                return ''
            else:
                return('- ' + str(coefficient * -1) + 'x')
    elif exponent > 1:
        if coefficient == 1:
            return('+ x^' + str(exponent))
        elif coefficient == -1:
            return('- x^' + str(exponent))
        else:
            if coefficient > 0:
                return('+ ' + str(coefficient) + 'x^' + str(exponent))
            elif coefficient == 0:
                return ''
            else:
                return('- ' + str(coefficient * -1) + 'x^' + str(exponent))

# ##############################################################################
# Polynom parser
# ##############################################################################

def cleanTerm(termInput):
    """Parser: clean the term"""
    term = termInput.replace(' ', '')
    if len(term) == 0:
        return term
    if term[-1] == '-' or term[-1] == '+':
        newTerm = term[:-1]
    else:
        newTerm = term
    if len(newTerm) == 0:
        return term
    if newTerm[0] == '+':
        return newTerm[1:]
    return newTerm

def termValid(term):
    """Parser: is term valid"""
    isX = False
    isV = False
    counterX = 0
    counterV = 0
    if len(term) == 0:
        return False
    if len(term) == 1:
        if term[0] == '-' or term[0] == '+' or term[0] == '^' or term[0] == ' ':
            return False
    for i in term:
        if i != '-' and i != '+' and i != 'x' and i != '^' and i != ' ' and not i.isdigit():
            return False
        if i == '^':
            if term[-1] == 'x':
                return False
            isV = True
            counterV += 1
        if i == 'x':
            isX = True
            counterX += 1
    if isV and not isX:
        return False
    if counterV > 1 or counterX > 1:
        return False
    return True

def parseTerm(termInput):
    """Parser: parse the term"""
    term = cleanTerm(termInput)
    if not termValid(term):
        print 'bad input'
        return None
    if '^' in term: # 3x^2 or -3x^2 or x^4 or -x^4
        parts = term.split('x')
        if len(parts[0]) > 0:
            if parts[0][0] == '-':
                if len(parts[0]) == 1: # '-' ^4
                    coefficient = -1
                else: # -3 ^2
                    coefficient = int(parts[0])
            else: # 3 ^2
                coefficient = int(parts[0])
        else: # '' ^4
            coefficient = 1
        exponent = int(parts[1][1:])
        return Term(coefficient, exponent)
    elif 'x' in term: # 2x or -4x or x or -x
        coefficient = term[:-1]
        if len(coefficient) == 0:
            return Term(1, 1)
        if len(coefficient) == 1 and coefficient[0] == '-':
            return Term(-1, 1)
        return Term(int(coefficient), 1)
    else:
        if term.isdigit(): # 42
            return Term(int(term), 0)
        elif term[0] == '-' and term[1:].isdigit(): # -24
            return Term(int(term), 0)
        else: # bad input
            print 'bad input'
            return None

# ##############################################################################
# Mandatory part
# ##############################################################################

class Term:
    """Class Term (data struct)"""
    def __init__(self, coefficient, exponent):
        self.coefficient = coefficient
        self.exponent = exponent

def showResult(polynom_1, polynom_2):
    """Show result from two dictionaries"""
    timeStart = time.time()
    print "\n>-----------< result >-----------<\n"
    for exponent, coefficient in polynom_1.iteritems():
        try:
            coefficient_2 = polynom_2.pop(exponent)
            if not BIG:
                print recreateTerm(coefficient + coefficient_2, exponent),
        except KeyError:
            if not BIG:
                print recreateTerm(coefficient, exponent),
    for exponent, coefficient in polynom_2.iteritems():
        if not BIG:
            print recreateTerm(coefficient, exponent),
    print
    debug('\n[Result] %2f' % ((time.time() - timeStart)) + ' seconds')

def getTerms(polynom, generator=False):
    """Create table from polynom (string)"""
    timeStart = time.time()
    termTable = {}

    if generator:
        while True:
            try:
                term = polynom.next()
            except StopIteration:
                break
            if term.exponent in termTable:
                termTable[term.exponent] += term.coefficient
            else:
                termTable[term.exponent] = term.coefficient
        print
        debug('\n[Generator] %2f' % ((time.time() - timeStart)) + ' seconds')
        return termTable

    lenght = len(polynom)
    beg = 0
    for index, char in enumerate(polynom):
        if char == '-' or char == '+' or index == lenght - 1:
            if index == 0 and index != lenght - 1:
                continue
            term = parseTerm(polynom[beg:index + 1])
            if term is not None:
                if term.exponent in termTable:
                    termTable[term.exponent] += term.coefficient
                else:
                    termTable[term.exponent] = term.coefficient
            beg = index
    debug('\n[Parser] %2f' % ((time.time() - timeStart)) + ' seconds')
    return termTable

# ##############################################################################
# main and helpers
# ##############################################################################

def showDocs():
    """Show __doc__ string of functions"""
    counter = 1
    print '\n--------------------------------------'
    print main.__doc__
    print showUsage.__doc__
    print showDocs.__doc__
    print getTerms.__doc__
    print showResult.__doc__
    print Term.__doc__
    print parseTerm.__doc__
    print termValid.__doc__
    print cleanTerm.__doc__
    print generatePolynom.__doc__
    print recreateTerm.__doc__
    print '--------------------------------------\n'

def debug(text):
    """Debug function"""
    if DEBUG:
        print text

def setDebug():
    global DEBUG
    if DEBUG:
        DEBUG = False
    else:
        DEBUG = True

def setBigMode():
    global BIG
    global DEBUG
    if BIG:
        DEBUG = False
        BIG = False
    else:
        DEBUG = True
        BIG = True

def showUsage():
    """Show usage"""
    print '\nusage:'
    print '\tpolynom.py <any flag>\trun in BIG mode: ' + str(BIGPOLYNOM) + ' terms\n'
    print "command line flags:"
    print "\t@ \tgenerate one term"
    print "\th \tshow usage"
    print "\ts \tshow __doc__ strings"
    print "\tb \tBIG mode <enable/disable>"
    print "\td \tdebug mode <enable/disable>"
    print "\t! \texit\n"
    if BIG: print 'BIG mode [enabled]'
    else: print 'BIG mode [disabled]'
    if DEBUG: print 'DEBUG mode [enabled]'
    else: print 'DEBUG mode [disabled]'
    print "\npolynom example: 2x^3 + x^2 - 5x + x - 10 + 1\n"
    print "enter command or polynom (tap <ENTER> for generate polynom):"

def main():
    """Main method"""
    os.system('clear')
    showUsage()
    terms = []
    while True:
        generator = False
        if len(terms) == 0:
            polynom = raw_input('\n-----< enter first polynom >------\n')
        else:
            polynom = raw_input('\n-----< enter second polynom >-----\n')
        length = len(polynom)
        if length == 0:
            generator = True
            if BIG:
                polynom = generatePolynom(BIGPOLYNOM, BIGPOLYNOM + 1, 100000)
            else:
                polynom = generatePolynom()
        elif length == 1 and '!' in polynom:
            print("exit OK")
            sys.exit(0)
        elif length == 1 and 'h' in polynom:
            showUsage()
            continue
        elif length == 1 and 'b' in polynom:
            setBigMode()
            main()
        elif length == 1 and 'd' in polynom:
            setDebug()
            main()
        elif length == 1 and 's' in polynom:
            showDocs()
            continue
        elif length == 1 and '@' in polynom:
            generator = True
            polynom = generatePolynom(1, 2)
        parsedPolynom = getTerms(polynom, generator)
        if len(parsedPolynom) != 0:
            terms.append(parsedPolynom)
        if len(terms) == 2:
            showResult(terms[0], terms[1])
            del terms[:]

if __name__ == '__main__':
    if len(sys.argv) > 1:
        setBigMode()
    main()
