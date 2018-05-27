#!/usr/bin/env bash

THIS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [ -e "$HOME/.nix-profile/etc/profile.d/nix.sh" ]; then source "$HOME/.nix-profile/etc/profile.d/nix.sh"; fi

# if [ -e "/nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh" ]; then source "/nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh"; fi

if [ -d "$HOME/.local/share/inaugurate/conda/envs/inaugurate/bin" ]; then
    export PATH="$HOME/.local/share/inaugurate/conda/envs/inaugurate/bin:$PATH"
fi
if [ -d "$HOME/.local/share/inaugurate/virtualenvs/inaugurate/bin" ]; then
    export PATH="$HOME/.local/share/inaugurate/virtualenvs/inaugurate/bin:$PATH"
fi
if [ -d "$HOME/.local/share/inaugurate/conda/bin" ]; then
    export PATH="$HOME/.local/share/inaugurate/conda/bin:$PATH"
fi
if [ -d "$HOME/.local/share/inaugurate/bin" ]; then
    export PATH="$HOME/.local/share/inaugurate/bin:$PATH"
fi
if [ -d "$HOME/.local/bin" ]; then
    export PATH="$HOME/.local/bin:$PATH"
fi

# additional bin paths
{% for path in  cookiecutter.extra_paths.split(':') %}
if [ -d "{{ path }}" ]; then
    export PATH="{{ path }}:$PATH"
fi
{% endfor %}

cd "${THIS_DIR}/plays"

{{cookiecutter.extra_script_commands}}

ansible-playbook {{cookiecutter.ansible_playbook_args}} {{cookiecutter.ask_sudo}} {{cookiecutter.playbook}}
