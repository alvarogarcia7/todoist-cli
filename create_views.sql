DROP VIEW IF EXISTS tasks;
CREATE VIEW tasks (id, project_name, content, description, created, processed)
AS
select tasks.id, projects.name, tasks.content, tasks.description, tasks.created_at, tasks.processed
from tasks_ tasks
         INNER JOIN projects on projects.id = tasks.project_id;

DROP VIEW IF EXISTS splitwise_lines;
CREATE VIEW splitwise_lines (type, Date, Description, Category, Cost, Currency, Other, Mine)
AS
select case
           when trim(Description) IN ('L p. paid alvaro', 'alvaro paid L p.', 'Transferencia', 'Transfer')
               then 'TRANSFER:DISCARD'
           when (Cost = alvaro) then 'LPG_PAY_ALL'
           when (Cost = `L pereira`) then 'AGB_PAY_ALL'
           when Category = 'Payment' then 'TRANSFER:DISCARD'
           else 'SHARED_EXPENSE'
           end as Type,
       Date,
       trim(Description),
       Category,
       Cost,
       Currency,
       "L pereira",
       alvaro
from splitwise_lines_;
