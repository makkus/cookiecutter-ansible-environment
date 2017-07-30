#!/usr/bin/env bash

if [ -e "$HOME/.nix-profile/etc/profile.d/nix.sh" ]; then source "$HOME/.nix-profile/etc/profile.d/nix.sh"; fi

cd {{cookiecutter.playbook_dir}}/../debug

{{cookiecutter.extra_script_commands}}

ANSIBLE_CONFIG=./ansible.cfg ansible-playbook -vvvv {{cookiecutter.ask_sudo}} ../plays/{{cookiecutter.playbook}}
