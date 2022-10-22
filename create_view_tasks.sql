DROP VIEW IF EXISTS tasks;
CREATE VIEW tasks (id, project_name, content, description, created, processed)
AS
select tasks.id, projects.name, tasks.content, tasks.description, tasks.created, tasks.processed
from tasks_ tasks
INNER JOIN projects on projects.id = tasks.project_id;