#pylint: disable = line-too-long, too-many-lines, no-name-in-module, import-error, multiple-imports, pointless-string-statement, wrong-import-order
import airflow
from datetime import timedelta,date,datetime
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from scripts.finance import YfinanceStock
from scripts.stock import stockData


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2021,2,28),
    'retries': 2,
    'retry_delay': timedelta(minutes=5)
}


dag = DAG(
    'marketvol',
    default_args=default_args,
    description='A simple DAG',
    #schedule_interval='0 18	* *	1,2,3,4,5'  # running from Mon-Fri at 6 PM
    schedule_interval='0 18	* *	*'  # running from Mon-Fri at 6 PM
)


templated_command="""
        cd $DATAPATH ; mkdir {{ ds }} ; cd .. ; cd finance_data ; mkdir {{ ds }}
"""

create_data_directory = BashOperator(
    task_id='create_data_directory',
    depends_on_past=False,
    bash_command=templated_command,
    dag=dag
)

today= "{{ ds }}"

download_tsla_stock = PythonOperator(
    task_id='download_tsla_stock', 
    python_callable=YfinanceStock.download_stock_data,
    op_kwargs={'symbolType':'tsla'},
    provide_context=True,
    dag=dag)


download_apple_stock = PythonOperator(
    task_id='download_apple_stock', 
    python_callable=YfinanceStock.download_stock_data,
    op_kwargs={'symbolType':'aapl'},
    provide_context=True,
    dag=dag)


templated_command="""
    mv $DATAPATH/{{ ds }}/{{ params.filename }}  /usr/local/finance_data/{{ ds }}
"""

move_tsla_data_to_diff_loc = BashOperator(
    task_id='move_tsla_data_to_diff_location',
    bash_command=templated_command,
    params={'filename': 'data_tsla.csv'},
    dag=dag
)


move_apple_data_to_diff_loc = BashOperator(
    task_id='move_apple_data_to_diff_location',
    bash_command=templated_command,
    params={'filename': 'data_aapl.csv'},
    dag=dag
)

connect = DummyOperator(
    task_id='connect',
    dag=dag
)

execute_query_on_data	= PythonOperator(
      task_id='execute_query_on_data', 
      python_callable=stockData.execute_query,
      provide_context=True,
      dag=dag
)


create_data_directory >> [download_tsla_stock,download_apple_stock] 

download_tsla_stock >> move_tsla_data_to_diff_loc

download_apple_stock >> move_apple_data_to_diff_loc

move_tsla_data_to_diff_loc >> connect

move_apple_data_to_diff_loc >> connect 

connect >> execute_query_on_data