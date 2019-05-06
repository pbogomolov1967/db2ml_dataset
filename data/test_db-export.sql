select 
	CONCAT('emp_no#', CONVERT(e.emp_no,char)) as emp_id, e.birth_date, e.gender, s.salary,
	t.title, s.to_date as salary_end_date, t.to_date as title_end_date
from employees e
	left join salaries s on e.emp_no = s.emp_no and e.hire_date = s.from_date
	left join titles t   on e.emp_no = t.emp_no and e.hire_date = t.from_date
where 	
	s.salary is not null
-- LIMIT 10
