from qiskit.visualization import circuit_drawer
from fastapi.responses import Response
from app.db.models.user import User
from fastapi import Depends,FastAPI
from app.services.auth import get_current_user


router = FastAPI()

@router.get("/visualize-circuit")
async def visualize_circuit(
    response_type: str = "text",
    current_user: User = Depends(get_current_user)
):
    """Returns quantum circuit diagram"""
    # Sample circuit
    qc = QuantumCircuit(3)
    qc.h([0,1,2])
    qc.cz(0,1)
    qc.cz(1,2)
    qc.measure_all()
    
    if response_type == "text":
        # ASCII art
        diagram = circuit_drawer(qc, output='text').single_string()
        return Response(content=diagram, media_type="text/plain")
    else:
        # SVG image
        diagram = circuit_drawer(qc, output='svg')
        return Response(content=diagram, media_type="image/svg+xml")