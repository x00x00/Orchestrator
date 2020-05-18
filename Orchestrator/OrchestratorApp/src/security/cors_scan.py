import requests
from ..mongo import mongo
from datetime import datetime
from .. import constants
from ..slack import slack_sender
import os
import subprocess
import json


def cleanup(path):
    try:
        os.remove(path)
    except FileNotFoundError:
        pass
    return


def handle_target(target, url_list, language):
    print('------------------- CORS SCAN STARTING -------------------')
    print('Found ' + str(len(url_list)) + ' targets to scan')
    slack_sender.send_simple_message("CORS scan started against target: %s. %d alive urls found!"
                                     % (target, len(url_list)))
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

    # We first put all the urls with http/s into a txt file
    FILE_WITH_URLS = ROOT_DIR + '/tools_output/' + url_list[0]['target'] + '.txt'
    cleanup(FILE_WITH_URLS)
    with open(FILE_WITH_URLS, 'w') as f:
        for item in url_list:
            f.write("%s\n" % item['url_with_http'])

    # Call scan target with the file
    scan_target(url_list[0]['target'], FILE_WITH_URLS, language)
    # Delete all created files
    cleanup(FILE_WITH_URLS)
    print('-------------------  CORS SCAN FINISHED -------------------')
    return


def handle_single(url, language):
    print('------------------- CORS SCAN STARTING -------------------')
    slack_sender.send_simple_message("CORS scan started against %s" % url)
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

    # Put urls in a single file
    only_host = url.split('/')[2]
    FILE_WITH_URL = ROOT_DIR + '/tools_output/' + only_host + '.txt'
    cleanup(FILE_WITH_URL)
    with open(FILE_WITH_URL, 'w') as f:
        f.write("%s\n" % url)

    # Call scan target
    scan_target(only_host, url, FILE_WITH_URL, language)

    # Delete all created files
    cleanup(FILE_WITH_URL)
    print('------------------- CORS SCAN FINISHED -------------------')
    return


def add_vulnerability(target_name, language, vuln):
    timestamp = datetime.now()
    if language == constants.LANGUAGE_ENGLISH:
        mongo.add_vulnerability(target_name, vuln['url'],
                                constants.CORS_ENGLISH,
                                timestamp, language, 'Found CORS %s with origin %s' % (vuln['type'], vuln['origin']))
    elif language == constants.LANGUAGE_SPANISH:
        mongo.add_vulnerability(target_name, vuln['url'],
                                constants.CORS_SPANISH,
                                timestamp, language, 'Se encontro CORS %s usando origin %s' % (vuln['type'], vuln['origin']))


def scan_target(target_name, plain_url, file_name, language):

    # Call the tool with the previous file
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    FILE_WITH_JSON_RESULT = ROOT_DIR + '/tools_output/' + target_name + '.json'
    TOOL_DIR = ROOT_DIR + '/tools/CORScanner/cors_scan.py'
    cleanup(FILE_WITH_JSON_RESULT)
    cors_process = subprocess.run(
        ['python3', TOOL_DIR, '-i', file_name, '-o', FILE_WITH_JSON_RESULT])
    
    with open(FILE_WITH_JSON_RESULT) as json_file:
        vulns = json.load(json_file)

    if not vulns:
        cleanup(FILE_WITH_JSON_RESULT)
        return

    for vuln in vulns:
        slack_sender.send_simple_vuln("CORS (%s) vulnerability found at %s" % (vuln['type'], plain_url))
        add_vulnerability(plain_url, language, vuln)

    cleanup(FILE_WITH_JSON_RESULT)
    return