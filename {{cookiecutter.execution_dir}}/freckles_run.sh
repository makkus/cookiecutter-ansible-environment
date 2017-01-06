#!/usr/bin/env bash
cd {{cookiecutter.freckles_playbook_dir}}
../extensions/setup/role_update.sh
ansible-playbook {{cookiecutter.freckles_install_playbook}}
ansible-playbook {{cookiecutter.freckles_stow_playbook}}
