from sqlalchemy import text
from fastapi import APIRouter, Depends, HTTPException
from src.api import auth
from src.database import engine
from pydantic import BaseModel


router = APIRouter(
    prefix="/data",
    tags=["hello"],
    dependencies=[Depends(auth.get_api_key)],
)

class CarData(BaseModel):
    now: float;
    rpm: float;
    speed: float;
    tacho: float;
    distance: float;
    voltage: float;
    temp_mos: float;
    temp_motor: float;
    current_motor: float;
    current_batt: float;
    net_energy: float;
    efficiency: float;
    avg_speed: float;
    elapsed: float;
    time_remaining: float;
    fault_code: int;

@router.post("")
def push_data(request: CarData):
    #TODO: Add timestamp
    # time = request.now`
    rpm = request.rpm
    speed = request.speed
    tacho = request.tacho
    distance = request.distance
    voltage = request.voltage
    temp_mos = request.temp_mos
    temp_motor = request.temp_motor
    current_motor = request.current_motor
    current_batt = request.current_batt
    net_energy = request.net_energy
    efficiency = request.efficiency
    avg_speed = request.avg_speed
    elapsed = request.elapsed
    time_remaining = request.time_remaining
    fault_code = request.fault_code 

    query = """
        INSERT INTO run_history
            (rpm, temp_motor, speed, tacho, distance, voltage, temp_mos, current_motor,
            current_batt, net_energy, efficiency, avg_speed, elapsed, time_remaining, fault_code)
            VALUES 
            (:rpm, :temp_motor, :speed, :tacho, :distance, :voltage, :temp_mos, :current_motor,
            :current_batt, :net_energy, :efficiency, :avg_speed, :elapsed, :time_remaining, :fault_code)
    """
    with engine.begin() as connection:
        connection.execute(text(query), {
            # "time": time,
            "rpm": rpm,
            "speed": speed,
            "tacho": tacho,
            "distance": distance,
            "voltage": voltage,
            "temp_mos": temp_mos,
            "temp_motor": temp_motor,
            "current_motor": current_motor,
            "current_batt": current_batt,
            "net_energy": net_energy,
            "efficiency": efficiency,
            "avg_speed": avg_speed,
            "elapsed": elapsed,
            "time_remaining": time_remaining,
            "fault_code": fault_code
        })
    return "success"

@router.get("")
def test():
    return "hi"