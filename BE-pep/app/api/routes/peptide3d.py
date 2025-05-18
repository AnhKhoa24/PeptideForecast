from fastapi import APIRouter
from pydantic import BaseModel
from PeptideBuilder import Geometry, PeptideBuilder
from Bio.PDB import PDBIO
from tempfile import NamedTemporaryFile

router = APIRouter()

class PeptideRequest(BaseModel):
    sequence: str

@router.post("/generate_pdb")
def generate_pdb(data: PeptideRequest):
    try:
        seq = data.sequence.upper()
        geo_list = [Geometry.geometry(res) for res in seq]
        phi = [-60] * len(seq)
        psi_im1 = [-45] * len(seq)
        structure = PeptideBuilder.make_structure(geo_list, phi, psi_im1)

        io = PDBIO()
        with NamedTemporaryFile("r+", suffix=".pdb", delete=False) as tmp:
            io.set_structure(structure)
            io.save(tmp.name)
            tmp.seek(0)
            return {"pdb": tmp.read()}
    except Exception as e:
        return {"error": str(e)}
