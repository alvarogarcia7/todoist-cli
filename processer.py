import json
from typing import Dict, List, Tuple, Iterator


# Project = Dict[str, int, str, int, bool, bool, int, bool, str]

class Tasks:
    def __init__(self, tasks):
        self.values: List[Dict[id: str]] = tasks

    def filter_by_project_id(self, project_id) -> List:
        return self._sort_by_created_ASC(
            filter(lambda task: task['project_id'] == project_id, self.values)
        )

    @staticmethod
    def _sort_by_created_ASC(tasks: Iterator) -> List:
        return sorted(tasks,
                      key=lambda task: task['created']
                      )


class Projects:
    def __init__(self, projects):
        self.values: List[Dict[id: str]] = projects

    def _filter_by_name(self, name: str):
        return list(filter(lambda project: project['name'].lower() == name, self.values))

    def inbox(self):
        return self._filter_by_name('inbox')[0]

    def today(self):
        return self._filter_by_name('today')

    def by_id(self, id: int):
        return self._filter_by_id(id)

    def by_name(self, name: str):
        return self._filter_by_name(name)

    def _filter_by_id(self, id: int):
        return list(filter(lambda project: project['id'] == id, self.values))


class Todoist:
    def __init__(self, tasks: Tasks, projects: Projects):
        self.projects: Projects = projects
        self.tasks: Tasks = tasks

    def all_tasks_of_project_name(self, project_name: str) -> List:
        project_id = self.projects.by_name(project_name)[0]['id']
        return self.tasks.filter_by_project_id(project_id)


def main(**kwargs):
    tasks_path = kwargs['tasks']
    projects_path = kwargs['projects']

    print(f"[Cache] Reading tasks from {tasks_path}")
    print(f"[Cache] Reading projects from {projects_path}")

    with open(tasks_path) as file:
        tasks = json.load(file)

    with open(projects_path) as file:
        projects = json.load(file)

    todoist: Todoist = Todoist(Tasks(tasks), Projects(projects))

    print("Tasks of project 'today'")
    for task in todoist.all_tasks_of_project_name('today'):
        print(task['content'])


if __name__ == '__main__':
    main(projects='./all_projects.json', tasks='./all_tasks.json')
