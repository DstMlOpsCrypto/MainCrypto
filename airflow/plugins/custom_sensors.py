# /opt/airflow/plugins/custom_sensors.py

from airflow.plugins_manager import AirflowPlugin
from airflow.sensors.base import BaseSensorOperator
from airflow.utils.session import provide_session
from airflow.models.dagrun import DagRun
from airflow.utils.state import DagRunState

class ExternalDagRunSensor(BaseSensorOperator):
    def __init__(self, external_dag_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.external_dag_id = external_dag_id

    @provide_session
    def poke(self, context, session=None):
        dag_run = session.query(DagRun).filter(
            DagRun.dag_id == self.external_dag_id,
            DagRun.state == DagRunState.SUCCESS,
        ).order_by(DagRun.execution_date.desc()).first()

        if dag_run:
            self.log.info(f"Found successful DAG run of {self.external_dag_id} at {dag_run.execution_date}")
            return True
        else:
            self.log.info(f"No successful DAG run found for {self.external_dag_id}")
            return False

class CustomSensorPlugin(AirflowPlugin):
    name = "custom_sensors"
    sensors = [ExternalDagRunSensor]
