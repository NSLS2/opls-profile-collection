#set_project_name("ocko")
#set_project_name("dutta")

def set_project_name(project_name):
    RE.md['project_name'] = project_name
    current_dir = proposal_path() + f"projects/{project_name}/"
    print(f'current working at {current_dir}')
