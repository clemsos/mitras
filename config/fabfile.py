"""Test script for article"""

from fabric.api import run

def set_up():
    """does some setup automation"""
    run('setup something')

def run():
    """main run method, that now calls set_up() method"""
    set_up()