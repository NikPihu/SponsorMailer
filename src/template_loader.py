import os
import random

TEMPLATE_DIR = "templates"

def load_templates():
    templates = []

    for i in range(1, 7):
        path = os.path.join(TEMPLATE_DIR, f"template_{i}.txt")
        with open(path, "r", encoding="utf-8") as f:
            templates.append(f.read())

    return templates


def get_random_template(templates):
    return random.choice(templates)


def personalize_template(template, company, hr):
    return template.replace("{company}", company).replace("{hr}", hr)