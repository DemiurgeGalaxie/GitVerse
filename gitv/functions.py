import pygit2

import os 

import os
import requests

def create_github_repo_and_push_local(token, repo_name, description="", private=True):
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }
    data = {
        "name": repo_name,
        "description": description,
        "private": private,
    }
    response = requests.post("https://api.github.com/user/repos", headers=headers, json=data)
    response.raise_for_status()
    remote_url = response.json()["clone_url"]

    if os.path.exists(repo_name):
        raise ValueError(f"A directory named '{repo_name}' already exists.")
    repo_path = os.path.join(os.getcwd(), repo_name)
    repo = pygit2.init_repository(repo_path)
    
    repo.remotes.add('origin', remote_url)

    credentials = pygit2.Keypair("git", "", "", token)
    callbacks = pygit2.RemoteCallbacks(credentials=credentials)
    repo.remotes['origin'].push(['refs/heads/master'], callbacks=callbacks)

    return remote_url


def create_file_as_submodule_and_push(main_repo_path, file_name, github_token):
    # Ensure the main repository exists
    if not os.path.exists(main_repo_path) or not os.path.isdir(main_repo_path):
        raise ValueError("Specified main repository path does not exist or is not a directory.")

    # Check if the file already exists in the main repository
    file_content = None
    original_file_path = os.path.join(main_repo_path, file_name)
    if os.path.exists(original_file_path):
        with open(original_file_path, 'r') as f:
            file_content = f.read()

    # Create and push the new submodule repository to GitHub
    submodule_remote_url = create_github_repo_and_push_local(github_token, file_name)

    # Create the actual file inside the submodule repo
    submodule_path = os.path.join(main_repo_path, file_name)
    with open(os.path.join(submodule_path, file_name), 'w') as f:
        if file_content:
            f.write(file_content)  # Write the content of the original file if it existed
        else:
            f.write('')  # Otherwise, create an empty file

    # Commit the file to the submodule repository
    submodule_repo = pygit2.Repository(submodule_path)
    submodule_index = submodule_repo.index
    submodule_index.add_all()
    submodule_index.write()
    tree = submodule_index.write_tree()
    author = pygit2.Signature("Author name", "author@email.com")
    committer = pygit2.Signature("Committer name", "committer@email.com")
    commit_message = f"Added {file_name}."
    submodule_repo.create_commit("HEAD", author, committer, commit_message, tree, [submodule_repo.head.target])

    # Add the submodule to the main repository
    main_repo = pygit2.Repository(main_repo_path)
    main_repo.submodules.add(file_name, file_name, url=submodule_remote_url)
    main_repo.submodules.save()

    # Commit the changes in the main repository
    index = main_repo.index
    index.add_all()
    index.write()
    tree = index.write_tree()
    main_repo.create_commit("HEAD", author, committer, f"Added {file_name} as a submodule.", tree, [main_repo.head.target])

    # If the original file existed, remove it
    if file_content:
        os.remove(original_file_path)
