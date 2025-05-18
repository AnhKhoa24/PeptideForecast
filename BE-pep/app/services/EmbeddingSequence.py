import math
import numpy as np
from Bio import SeqIO
import pandas as pd
from io import StringIO
from fastapi import UploadFile
def generate_vector(sequence):
    properties = {
        "hydrophobicity": {
            "polar": "RKEDQN",
            "neutral": "GASTPHY",
            "hydrophobic": "CLVIMFW"
        },
        "vdw_volume": {
            "small": "GASTPDC",
            "medium": "NVEQIL",
            "large": "MHKFRYW"
        },
        "polarity": {
            "polar": "EDQNKR",
            "neutral": "GASTPHY",
            "nonpolar": "CLVIMFW"
        },
        "polarizability": {
            "low": "GASDT",
            "medium": "CPNVEQIL",
            "high": "KMHFRYW"
        },
        "charge": {
            "negative": "DE",
            "neutral": "ACFGHILMNPQSTVWY",
            "positive": "KR"
        },
        "secondary_structure": {
            "helix": "EALMQKRH",
            "sheet": "VIYCWT",
            "coil": "GNPSD"
        },
        "solvent_accessibility": {
            "buried": "ALFCGIVW",
            "intermediate": "MPSTHY",
            "exposed": "DEKNQR"
        }
    }

    def calculate_distribution(amino_class):
        class_residues = [i for i, aa in enumerate(sequence) if aa in amino_class]
        length = len(sequence)
        total = len(class_residues)

        if total == 0:
            return [0.0] * 6

        values = []
        for p in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]:
            idx = math.floor(total * p)
            if idx >= total:
                idx = total - 1
            pos = class_residues[idx]
            values.append((pos + 1) / length * 100)
        return values

    matrix = []

    for prop_name in properties:
        row = []
        for class_name in properties[prop_name]:
            aa_group = properties[prop_name][class_name]
            dist = calculate_distribution(aa_group)
            row.extend(dist)  # mỗi lớp 6 mốc
        matrix.append(row)  # 3 lớp → 18 feature / 1 prop

    return np.array(matrix)  # shape (7, 18)

def fasta_to_dataframe(fasta_bytes: bytes):
    fasta_io = StringIO(fasta_bytes.decode())
    data = []
    for record in SeqIO.parse(fasta_io, "fasta"):
        seq_id = record.id.split()[0]
        sequence = str(record.seq)
        data.append({
            "ID": seq_id,
            "Sequence": sequence
        })
    return pd.DataFrame(data)

async def parse_fasta_and_filter(upload_file: UploadFile):
    content = await upload_file.read()
    fasta_io = StringIO(content.decode())

    valid_records = []
    skipped_records = []

    for record in SeqIO.parse(fasta_io, "fasta"):
        sequence = str(record.seq).strip()
        if 10 <= len(sequence) <= 50:
            valid_records.append(record)
        else:
            skipped_records.append(record)

    def records_to_fasta(records):
        handle = StringIO()
        SeqIO.write(records, handle, "fasta")
        return handle.getvalue().encode()

    return records_to_fasta(valid_records), records_to_fasta(skipped_records)

def transform_batch_3d(X_raw: np.ndarray, scaler, n_steps=7, n_features=18):
    X_flat = X_raw.reshape(-1, n_features)  # (N*7, 18)
    X_scaled = scaler.transform(X_flat)
    return X_scaled.reshape(-1, n_steps, n_features)
