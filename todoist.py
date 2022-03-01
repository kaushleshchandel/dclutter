#api = TodoistAPI('1697bd344b2b5fd64e675fa099c7a389ef729637')

# Use the todoist API to get tasks from the current day

from todoist_api_python.api import TodoistAPI
api = TodoistAPI('1697bd344b2b5fd64e675fa099c7a389ef729637')


try:
    tasks = api.get_tasks()
    for i in tasks:
        print(i.content)
except Exception as error:
    print(error)


#[Task(comment_count=0, completed=False, content='Please file the taxes', created='2022-02-25T13:14:08.995086Z', creator=1474165, description='', id=5628626764, project_id=2000398123, 
#section_id=0, priority=1, url='https://todoist.com/showTask?id=5628626764', assignee=None, assigner=0, due=Due(date='2022-03-01', recurring=False, string='Mar 1', datetime=None, timezone=None), 
#label_ids=[], order=9, parent_id=None, sync_id=None), 
