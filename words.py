# -*- coding: utf-8 -*-
"""
Created on Tue Feb  5 09:25:23 2019

@author: sbergmann

Copyright@Hach Lange GmbH 
"""
s1 = "NJRETTHGERKVOGERJCWGRUJAANJFNJEWNAFJSDNFOGERJCWERWETTDJKFGDNOGERJCWERWETTJFNJEWNAFJSDNFOGERJT"
s2 = "OGERJCWERWETTJFNJEWNAFJSDNFOGERJCHJNTJFNJEWNAFJSDNFOGERJT"

def shouldFindStringMatches(s1,s2):
    erg = [""]
    for i1 in range(len(s1)):
        for i2 in range(len(s2)):
            if s1[i1] == s2[i2]:
                ii1 = i1+1
                ii2 = i2+1
                s3 = s2[i2]
                while (ii2<len(s2) and ii1<len(s1)):
                    if(s1[ii1] == s2[ii2]):
                        s3 = s3 + s1[ii1]
                        ii1 = ii1+1
                        ii2 = ii2+1
                    else:
                        break
                if len(s3)>len(erg[0]):
                    erg=[s3]
                elif((len(s3)==len(erg[0])) and (s3 not in erg)):
                    erg.append(s3)
    return erg
print(shouldFindStringMatches(s1,s2))