from __future__ import absolute_import
import mock

from exporter import main, tasks


class TestTask(tasks.OrgTask, tasks.Task):
    NAME = 'test_task'
    EXT = 'csv'

def test_get_selected_tasks_no_options_org_tasks():
    assert [tasks.OrgEmailOptInTask] == main._get_selected_tasks(tasks.OrgTask, [], [])


def test_get_selected_tasks_no_options_course_tasks():
    default_tasks = sorted(
        [
            task for task in tasks.DEFAULT_TASKS if issubclass(task, tasks.CourseTask)
        ],
        key=lambda task: task.NAME
    )
    selected_tasks = sorted(
        main._get_selected_tasks(tasks.CourseTask, [], []),
        key=lambda task: task.NAME
    )
    assert default_tasks == selected_tasks


def test_get_selected_tasks_specified_from_options():
    assert [tasks.OrgEmailOptInTask] == main._get_selected_tasks(tasks.Task, ['OrgEmailOptInTask'], [])


def test_get_selected_tasks_excluded_tasks():
    default_tasks = sorted(
        set(tasks.DEFAULT_TASKS) - set([tasks.OrgEmailOptInTask]),
        key=lambda task: task.NAME
    )
    selected_tasks = sorted(
        main._get_selected_tasks(tasks.Task, [], ['OrgEmailOptInTask']),
        key=lambda task: task.NAME
    )
    assert default_tasks == selected_tasks



def test_run_tasks_happy_path():
    with mock.patch('os.path.isdir', return_value=True):
        kwargs = {
            'dry_run': False,
            'name': 'test-analytics',
            'work_dir': '/the/workdir/',
            'organization': 'testx',
        }
        results = main.run_tasks([TestTask], **kwargs)

        expected_results = [TestTask.get_filename(**kwargs)]
        assert expected_results == results
