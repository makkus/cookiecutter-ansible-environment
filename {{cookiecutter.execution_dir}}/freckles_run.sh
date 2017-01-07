#!/usr/bin/env bash

function update_roles {
    ../extensions/setup/role_update.sh
}

cd {{cookiecutter.freckles_playbook_dir}}
if [ ! -d ../roles/external/ansible-freckles ]; then
    update_roles
fi

ansible-playbook {{cookiecutter.freckles_ask_sudo}} {{cookiecutter.freckles_install_playbook}}
ansible-playbook {{cookiecutter.freckles_stow_playbook}}
