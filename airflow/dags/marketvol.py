#pylint: disable = line-too-long, too-many-lines, no-name-in-module, import-error, multiple-imports, pointless-string-statement, wrong-import-order
import airflow
from datetime import timedelta,date,datetime
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from scripts.finance import YfinanceStock
from scripts.stock import stockData

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2021, 2, 24),
    'retries': 2,
    'retry_delay': timedelta(minutes=5)
}


dag = DAG(
    'marketvol',
    default_args=default_args,
    description='A simple DAG',
    schedule_interval='0 18	* *	1,2,3,4,5'  # running from Mon-Fri at 6 PM
)

templated_command="""
        cd $DATAPATH ; mkdir {{ ds }}
"""
t0 = BashOperator(
    task_id='create_data_directory',
    depends_on_past=False,
    bash_command=templated_command,
    dag=dag
)


t1	= PythonOperator(
    task_id='download_yahoo_stock', 
    python_callable=YfinanceStock.download_stock_data,
    op_kwargs={'symbolType':'tsla'},
    dag=dag)


t2	= PythonOperator(
    task_id='download_apple_stock', 
    python_callable=YfinanceStock.download_stock_data,
    op_kwargs={'symbolType':'aapl'},
    dag=dag)


templated_command="""
        {% for filename in params.filenames %}
          mv $DATAPATH/{{ ds }}/{{ filename }}  /usr/local/finance_data
        {% endfor %}
  """

t3 = BashOperator(
    task_id='move_files_to_another_loc',
    bash_command=templated_command,
    params={'filenames': ['data_tsla.csv','data_aapl.csv']},
    dag=dag
)


t4	= PythonOperator(
      task_id='execute_query_on_data', 
      python_callable=stockData.execute_query,
      dag=dag
)


t0 >> t1 >> t2 >> t3 >> t4