import json
import logging
import os
import time

import requests
from signalrcore.hub_connection_builder import HubConnectionBuilder

from database import init_db, engine, db_session
from models import OxygenData


class Main:
    def __init__(self):
        self._hub_connection = None
        self.HOST = os.getenv("HOST", "http://34.95.34.5")  # Setup your host here
        self.TOKEN = os.getenv("TOKEN")  # Setup your token here
        self.TICKETS = os.getenv("TICKETS", 1)  # Setup your tickets here
        self.T_MAX = os.getenv("T_MAX", 30)  # Setup your max temperature here
        self.T_MIN = os.getenv("T_MIN", 20)  # Setup your min temperature here
        self.DATABASE = os.getenv(
            "DATABASE", "sqlite:///C:\\dblabo.db"
        )  # Setup your database here
        if self.TOKEN == None:
            raise Exception("Token need to be initialized in environment variables")

    def __del__(self):
        if self._hub_connection != None:
            self._hub_connection.stop()

    def setup(self):
        make_db()
        self.setSensorHub()

    def start(self):
        self.setup()
        self._hub_connection.start()

        print("Press CTRL+C to exit")
        while True:
            time.sleep(2)

    def setSensorHub(self):
        self._hub_connection = (
            HubConnectionBuilder()
            .with_url(f"{self.HOST}/SensorHub?token={self.TOKEN}")
            .configure_logging(logging.INFO)
            .with_automatic_reconnect(
                {
                    "type": "raw",
                    "keep_alive_interval": 10,
                    "reconnect_interval": 5,
                    "max_attempts": 999,
                }
            )
            .build()
        )

        self._hub_connection.on("ReceiveSensorData", self.onSensorDataReceived)
        self._hub_connection.on_open(lambda: print("||| Connection opened."))
        self._hub_connection.on_close(lambda: print("||| Connection closed."))
        self._hub_connection.on_error(
            lambda data: print(f"||| An exception was thrown closed: {data.error}")
        )

    def onSensorDataReceived(self, data):
        try:
            # print(data[0]["date"] + " --> " + data[0]["data"])
            date = data[0]["date"]
            dp = float(data[0]["data"])
            action = self.analyzeDatapoint(date, dp)
            self.send_event_to_database(date, dp, action)
        except Exception as err:
            print(err)

    def analyzeDatapoint(self, date, data):
        if float(data) >= float(self.T_MAX):
            return self.sendActionToHvac(date, "TurnOnAc", self.TICKETS)
        elif float(data) <= float(self.T_MIN):
            return self.sendActionToHvac(date, "TurnOnHeater", self.TICKETS)
        return ""

    def sendActionToHvac(self, date, action, nbTick):
        r = requests.get(f"{self.HOST}/api/hvac/{self.TOKEN}/{action}/{nbTick}")
        details = json.loads(r.text)
        return details["Response"]

    def send_event_to_database(self, timestamp, event, action):
        try:
            print(timestamp)
            print(event)
            print(action)
            db_session.add(OxygenData(timestamp=timestamp, temp=event, message=action))
            db_session.commit()
            # To implement
            pass
        except requests.exceptions.RequestException as e:
            # To implement
            pass


def make_db():
    print("creating the database...")
    init_db()
    con = engine.connect()


if __name__ == "__main__":
    main = Main()
    main.start()
