#!/usr/bin/env bash

cd {{cookiecutter.freckles_playbook_dir}}

ansible-playbook {{cookiecutter.freckles_ask_sudo}} {{cookiecutter.freckles_playbook}}
