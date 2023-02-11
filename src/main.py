# Provides the main entry point for the application, including:
# - Initial configuration using config.json
# - Flask app that serves the web app
# - Main loop that replaces flags using service plugins


import json
import os
import time
import traceback
import uuid
import importlib


from flask import Flask, render_template, request, redirect
from threading import Thread

from os.path import dirname, basename, isfile, join
import glob

from modules import *



config = {}
modules = {}

app = Flask(__name__)

def load_config():
    global config
    """Loads the configuration from config.json"""
    with open("../config/config.json", "r") as f:
        config = json.load(f)


def load_modules():
    """Loads all the service plugins from the modules directory"""
    global modules

    # For each .py file in the modules directory, import it and add it to the modules dictionary
    module_files = glob.glob(join(dirname(__file__), "modules", "*.py"))
    modules = { basename(f)[:-3]: importlib.import_module("modules." + basename(f)[:-3]) for f in module_files if isfile(f) and not f.endswith('__init__.py')}
    print(modules)




def generate_flag():
    """Generates a flag for a service and team"""
    return "flag{" + str(uuid.uuid4()) + "}"



def plant_flags():
    """Plants flags on all services on each box"""
    global config, modules
    for instance in config["instances"]:
            try:
                print("Planting flag on " + instance + ":" + str(config["instances"][instance]["port"]))
                flag = generate_flag()
                if modules[config["instances"][instance]["type"]].plant(flag, instance, config["instances"][instance]["port"], config["instances"][instance]["username"], config["instances"][instance]["password"]):
                    config["instances"][instance]["flag"] = flag
                    print("Planted flag " + flag + " on " + instance + ":" + str(config["instances"][instance]["port"]))
                else:
                    print("Error planting flag on " + instance + ":" + str(config["instances"][instance]["port"]))
            except Exception as e:
                print("Error planting flag on " + instance + ":" + str(config["instances"][instance]["port"]) + ": " + str(e))
                traceback.print_exc()


def check_flags():
    """Checks if flags are still on all services on each box"""
    global config, modules
    for instance in config["instances"]:
            try:
                result = modules[config["instances"][instance]["type"]].check(config["instances"][instance]["flag"], instance, config["instances"][instance]["port"], config["instances"][instance]["username"], config["instances"][instance]["password"])
                if result:
                    config["teams"][config["instances"][instance]["team"]]["score"] += config["points"]["uptime"]
                    print("Flag " + config["instances"][instance]["flag"] + " is still on " + instance + ":" + str(config["instances"][instance]["port"]))
                else:
                    print("Flag " + config["instances"][instance]["flag"] + " is not on " + instance + ":" + str(config["instances"][instance]["port"]))
            except Exception as e:
                print("Error checking flag on " + instance + ":" + str(config["instances"][instance]["port"]) + ": " + str(e))
                traceback.print_exc()



def flag_check_thread():
    """Thread that checks flags based on config.json interval"""
    global config, boxes
    while True:
        check_flags()
        time.sleep(config["intervals"]["flag_check"])
    

def flag_plant_thread():
    """Thread that plants flags based on config.json interval"""
    global config, boxes
    while True:
        plant_flags()
        time.sleep(config["intervals"]["flag_plant"])


# Flask app
@app.route("/")
def index():
    """Renders the templated page with following variables:"""
    global config
    # Set template directory to the templates directory
    app.template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
    # Render the index.html template with the following variables
    return render_template("index.html", config=config)

@app.route("/submit", methods=["POST"])
def submit():
    """Handles flag submission"""
    global config
    # Get the flag from the POST request
    flag = request.form["flag"]
    team = request.form["team"]
    # Check if the flag is valid
    for instance in config["instances"]:
        if config["instances"][instance]["flag"] == flag and config["instances"][instance]["team"] != team and flag not in config["teams"][team]["captured"]:
            # If the flag is valid, add points to the team
            config["teams"][team]["score"] += config["points"]["flag"]
            # Add the flag to the team's list of captured flags
            config["teams"][team]["captured"].append(flag)
    # Redirect to the index page
    return redirect("/")



def main():
    """Main entry point for the application"""
    global config, modules
    # Load the configuration
    load_config()

    # Load the service plugins
    load_modules()

    # Start the flag check thread
    t = Thread(target=flag_check_thread)
    t.start()


    # Start the flag plant thread
    t = Thread(target=flag_plant_thread)
    t.start()

    # Start the Flask app
    app.run(host="0.0.0.0", port=8082)

    # Wait for the threads to finish
    while True:
        time.sleep(10)

if __name__ == "__main__":
    main()