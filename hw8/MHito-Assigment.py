# MODULE 8 - 100 points total

import os
import json
from airflow import DAG
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta

# define the default arguments
default_args = {
    'owner': 'data_engineer',
    'start_date': datetime(2023, 4, 6),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

# define the DAG
with DAG('process_student_data', default_args=default_args, schedule_interval='@daily') as dag:

    def load_data():
        file_path = "/home/jhu/airflow/dags/data/input.json"  # Use absolute path
        with open(file_path, "r") as f:
            data = json.load(f)
        return data

    def process_data():
        data = load_data()
        students = data['students']
        courses = data['courses']

        # Nothing required here for submission - this function is complete
 

    def check_weekday(**context):
        execution_date = context['ds']
        
        # QUESTION #1 (20 points)
        # Extract the day (number) of the week
        date_obj = datetime.strptime(execution_date, "%Y-%m-%d")
        weekday = date_obj.weekday()

        if weekday < 5:  # weekday is 0-based, with 0=Monday and 4=Friday
            return 'store_data_weekday'
        else:
            return 'store_data_weekend'

        # QUESTION #2 (20 points)
        # Loop through the students and find each course and description
        # Save this data to the 'data/weekday_data.txt' file as follows:
        # '<LASTNAME, FIRSTNAME> took <COURSE> (<COURSE_DESCRIPTION>) on a weekday'
        # Example: 'Mosko, Scott took ENG101 (Data Engineering) on a weekday'
        # 
        # Each entry should be on a new line
        # This function is only run on weekdays (due to the check_weekday function)
    def store_data_weekday():
        data = load_data()
        students = data['students']
        courses = {course["name"]: course["description"] for course in data["courses"]}  # Create a dictionary for quick lookup

        output_lines = []

        for student in students:
            last_name, first_name = student["name"].split(" ", 1)  # Split into last and first name
            for course in student["courses"]:
                course_description = courses.get(course, "No description available")  # Get course description
                output_lines.append(f"{last_name}, {first_name} took {course} ({course_description}) on a weekday")

    # Write to file
        output_file_path = "/home/jhu/airflow/dags/data/weekday_data.txt"
        with open(output_file_path, "w") as f:
            f.write("\n".join(output_lines))

        print(f"Data successfully written to {output_file_path}")


    def store_data_weekend():
        data = load_data()
        students = data['students']
        courses = {course["name"]: course["description"] for course in data["courses"]}  # Dictionary for quick lookup

        output_lines = []

        for student in students:
            last_name, first_name = student["name"].split(" ", 1)  # Extract last and first name
            for course in student["courses"]:
                course_description = courses.get(course, "No description available")  # Get course description
                output_lines.append(f"{last_name}, {first_name} took {course} ({course_description}) on a weekend")

    # Write to file
        output_file_path = os.path.join(os.path.dirname(__file__), "data/weekend_data.txt")
        with open(output_file_path, "w") as f:
            f.write("\n".join(output_lines))

        print(f"Data successfully written to {output_file_path}")
        
        
        # QUESTION #3 (20 points)
        # Loop through the students and find each course and description
        # Save this data to the 'data/weekend_data.txt' file as follows:
        # '<LASTNAME, FIRSTNAME> took <COURSE> (<COURSE_DESCRIPTION>) on a weekend'
        # Example: 'Mosko, Scott took ENG101 (Data Engineering) on a weekend'
        # 
        # Each entry should be on a new line
        # This function is only run on weekends (due to the check_weekdend function)


    # QUESTION #4
    load_data_task = PythonOperator(
        task_id="load_data",
        python_callable=load_data,
        dag=dag
    )
    process_data_task = PythonOperator(
        task_id="process_data",
        python_callable=process_data,
        dag=dag
    )
    check_weekday_task = BranchPythonOperator(
        task_id="check_weekday",
        python_callable=check_weekday,
        provide_context=True,
        dag=dag
    )
    store_data_weekday_task = PythonOperator(
        task_id="store_data_weekday",
        python_callable=store_data_weekday,
        dag=dag
    )
    store_data_weekend_task = PythonOperator(
        task_id="store_data_weekend",
        python_callable=store_data_weekend,
        dag=dag
    )
    end_task = DummyOperator(
        task_id="end_task",
        dag=dag,
        trigger_rule="none_failed_min_one_success"  # Ensures it runs if at least one branch is successful
    )

    # Define task dependencies
    load_data_task >> process_data_task >> check_weekday_task
    check_weekday_task >> [store_data_weekday_task, store_data_weekend_task]  # Branching
    store_data_weekday_task >> end_task
    store_data_weekend_task >> end_task
        # Note that end_task will be tricky. There is a way to make it complete even though
        # only one of the branches finishes successfully and the other is skipped. Normally
        # this would cause anything following the branch to be skipped.

    # QUESTION #5 (20 points)
    # Create the flow for the DAG to match the provided diagram.

    # PLEASE NOTE: See Instruction document for files to turn in.