virtualenv venv<br/>
source venv/bin/activate<br/>

pip install 'apache-airflow==2.5.0' \
 --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.5.0/constraints-3.10.txt"<br/>
pip install numpy<br/>
pip install pandas<br/>
pip install tweepy<br/>

export AIRFLOW_HOME=$(pwd)<br/>
airflow db init<br/>
airflow users create --username admin --firstname admin\<br/>
    --lastname admin --role Admin --email x@gmail.com\<br/>
    --password admin<br/>

# create the etl pipeline
airflow standalone