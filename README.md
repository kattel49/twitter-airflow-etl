virtualenv venv
source venv/bin/activate

pip install 'apache-airflow==2.5.0' \
 --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.5.0/constraints-3.10.txt"
pip install numpy
pip install pandas
pip install tweepy

export AIRFLOW_HOME=$(pwd)
airflow db init
airflow users create --username admin --firstname admin\
    --lastname admin --role Admin --email x@gmail.com\
    --password admin

# create the app
airflow standalone