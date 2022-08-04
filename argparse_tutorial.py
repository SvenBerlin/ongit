# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 12:17:31 2022

@author: sbergmann
"""

import argparse


parser = argparse.ArgumentParser(description='A tutorial of argparse!')
parser.add_argument("--a", default=1, type=int, help="This is the 'a' variable")
parser.add_argument("--education", 
                    choices=["highschool", "college", "university", "other"],
                    required=True, type=str, help="Your name")

args = parser.parse_args()

ed = args.education

if ed == "college" or ed == "university":
    print("Has degree")
elif ed == "highschool":
  print("Finished Highschool")
else:
    print("Does not have degree")

input('press any key to finish')