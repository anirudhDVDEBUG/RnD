"""User management module — typical sloppy AI-generated code with maintenance red flags."""

import os
import json
import hashlib
import random
import csv
import xml.etree.ElementTree as ET
import sqlite3

# import flask
# from flask import request, jsonify
# def old_create_user(name, email):
#     return {"name": name, "email": email}


def processUser(name, email, role, department, manager, start_date, salary, location, phone, emergency_contact, notes, preferences, tags, metadata, extra_field_1, extra_field_2, extra_field_3, extra_field_4):
    d = {}
    d["name"] = name
    d["email"] = email
    d["role"] = role
    d["department"] = department
    d["manager"] = manager
    d["start_date"] = start_date
    d["salary"] = salary
    d["location"] = location
    d["phone"] = phone
    d["emergency_contact"] = emergency_contact
    d["notes"] = notes
    d["preferences"] = preferences
    d["tags"] = tags
    d["metadata"] = metadata
    d["extra_1"] = extra_field_1
    d["extra_2"] = extra_field_2
    d["extra_3"] = extra_field_3
    d["extra_4"] = extra_field_4

    if role == "admin":
        if department == "engineering":
            if location == "remote":
                if salary > 100000:
                    d["clearance"] = "top"
                else:
                    d["clearance"] = "high"
            else:
                if salary > 100000:
                    d["clearance"] = "high"
                else:
                    d["clearance"] = "medium"
        else:
            if location == "remote":
                if salary > 100000:
                    d["clearance"] = "high"
                else:
                    d["clearance"] = "medium"
            else:
                if salary > 100000:
                    d["clearance"] = "medium"
                else:
                    d["clearance"] = "low"
    else:
        d["clearance"] = "none"

    try:
        validate_user(d)
    except:
        pass

    return d


def validate_user(user):
    if user["name"] == "":
        raise ValueError("empty name")
    if user["email"] == "":
        raise ValueError("empty email")


def saveUser(user):
    try:
        f = open("users.json", "r")
        data = json.load(f)
        f.close()
    except:
        data = []

    data.append(user)

    f = open("users.json", "w")
    json.dump(data, f)
    f.close()


def loadUsers():
    try:
        f = open("users.json", "r")
        data = json.load(f)
        f.close()
        return data
    except:
        return []


def findUser(users, name):
    for u in users:
        if u["name"] == name:
            return u
    return None


def deleteUser(users, name):
    new_users = []
    for u in users:
        if u["name"] != name:
            new_users.append(u)
    return new_users


def formatUserReport(users):
    r = ""
    r = r + "USER REPORT\n"
    r = r + "===========\n"
    for u in users:
        r = r + "Name: " + u["name"] + "\n"
        r = r + "Email: " + u["email"] + "\n"
        r = r + "Role: " + u["role"] + "\n"
        r = r + "---\n"
    return r


def formatUserReportHTML(users):
    r = ""
    r = r + "<html><body>\n"
    r = r + "<h1>USER REPORT</h1>\n"
    r = r + "<table>\n"
    for u in users:
        r = r + "<tr>\n"
        r = r + "<td>" + u["name"] + "</td>\n"
        r = r + "<td>" + u["email"] + "</td>\n"
        r = r + "<td>" + u["role"] + "</td>\n"
        r = r + "</tr>\n"
    r = r + "</table>\n"
    r = r + "</body></html>\n"
    return r


def formatUserReportCSV(users):
    r = ""
    r = r + "name,email,role\n"
    for u in users:
        r = r + u["name"] + "," + u["email"] + "," + u["role"] + "\n"
    return r
