from fastapi import APIRouter, BackgroundTasks
from app.simulator.runner import start_simulation
from app.simulator.schemas import SimulationConfig

router = APIRouter(prefix="/admin/simulate", tags=["simulation"])

@router.post("/start")
def start_simulation_api(
    config: SimulationConfig,
    background_tasks: BackgroundTasks
):
    background_tasks.add_task(start_simulation, config)
    return {"status": "simulation_started"}
