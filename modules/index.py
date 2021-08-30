from flask import redirect, render_template, Flask, request, url_for, send_file
import datetime, json, os, dateutil, requests, subprocess
import glob

def checkX(string,negchecks,poschecks):
    checklist = []
    for x in negchecks:
        if x not in string:
            checklist.append(1)
        else:
            checklist.append(0)
    for x in poschecks:
        if x in string:
            checklist.append(1)
        else:
            checklist.append(0)
    if 0 in checklist:
        return False
    return True

def run_fast_scandir(dir, ext):    # dir: str, ext: list
    subfolders, files = [], []

    for f in os.scandir(dir):
        if f.is_dir():
            subfolders.append(f.path)
        if f.is_file():
            if os.path.splitext(f.name)[1].lower() in ext:
                files.append(f.path)


    for dir in list(subfolders):
        sf, f = run_fast_scandir(dir, ext)
        subfolders.extend(sf)
        files.extend(f)
    return subfolders, files