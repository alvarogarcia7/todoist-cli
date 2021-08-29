import json
from typing import Dict, List, Tuple, Iterator, Optional
import argparse
from datetime import date, timedelta, datetime, timezone
from dateutil import parser as dateutil_parser


# Project = Dict[str, int, str, int, bool, bool, int, bool, str]

class Tasks:
    def __init__(self, tasks):
        self.values: List[Dict[str]] = tasks

    def filter_by_project_id(self, project_id) -> List:
        return self._sort_by_created_ASC(
            filter(lambda task: task['project_id'] == project_id and task['section_id'] == 0, self.values)
        )

    @staticmethod
    def _sort_by_created_ASC(tasks: Iterator) -> List:
        return sorted(tasks,
                      key=lambda task: task['created']
                      )

    def filter_by_date(self, date_value: datetime) -> List:
        self._add_created_date()

        result = []
        for task in self.values:
            if task['created_date'] <= date_value:
                result.append(task)

        result = self._sort_by_created_date_DESC(result)

        return result

    @staticmethod
    def _sort_by_created_date_DESC(result):
        result = sorted(result, key=lambda task: task['created_date'], reverse=True)
        return result

    def _add_created_date(self):
        for task in self.values:
            task_date: date = dateutil_parser.parse(task['created'])
            task['created_date'] = task_date


class Projects:
    def __init__(self, projects):
        self.values: List[Dict[str]] = projects

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

    def all_tasks_due(self, duedate: str) -> List:
        if duedate == 'today':
            desired_date = datetime.now(tz=timezone.utc)
        elif duedate == 'yesterday':
            desired_date = (datetime.now(tz=timezone.utc) - timedelta(days=1))
        else:
            desired_date = datetime.fromisoformat(duedate)

        return self.tasks.filter_by_date(desired_date)

    @staticmethod
    def limit(results, limit):
        if limit is None:
            return results
        else:
            return results[:limit]


def main(args):
    print(args)
    projects_path = args.projects_path
    tasks_path = args.tasks_path

    print(f"[Cache] Reading tasks from {tasks_path}")
    print(f"[Cache] Reading projects from {projects_path}")

    with open(tasks_path) as file:
        tasks = json.load(file)

    with open(projects_path) as file:
        projects = json.load(file)

    todoist: Todoist = Todoist(Tasks(tasks), Projects(projects))

    if args.project:
        print(f"Tasks of project '{args.project}' (sorted date DESC):")
        for task in todoist.limit(todoist.all_tasks_of_project_name(args.project), args.limit):
            print(task['content'])
    elif args.due:
        if args.limit is None:
            args.limit = 10
        print(f"Tasks due '{args.due}' (sorted date ASC), (limit= {args.limit}):")
        for task in todoist.limit(todoist.all_tasks_due(args.due), args.limit):
            print(f"{task['created']}: {task['content']}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # Configuration
    parser.add_argument("-t", "--tasks_path", default='./all_tasks.json',
                        help="file path to read tasks")
    parser.add_argument("-p", "--projects_path", default='./all_projects.json',
                        help="file path to read projects")

    # Filters
    parser.add_argument("--project", help="filter by project name")
    parser.add_argument("--due", type=str, help="filter by task due date")
    parser.add_argument("--limit", type=int, help="limit results")

    main(parser.parse_args())
